"""Weekly marketing report command.

Hard-timeout every stage. Log stage boundaries to stderr (line-buffered on Railway).
Global 10-minute watchdog via SIGALRM: if any single run exceeds the budget, the
watchdog logs the current stage name and force-exits non-zero. Prior versions of
this command hung silently for months because a single outbound HTTP call blocked
forever with no restart policy to reap it.
"""
import logging
import os
import signal
import sys
import time

from django.core.management.base import BaseCommand

log = logging.getLogger('cron')

WATCHDOG_SECONDS = 600  # 10 minutes total
_current_stage = 'startup'


def _configure_logging():
    """Ensure logs are line-buffered and reach Railway immediately."""
    try:
        sys.stdout.reconfigure(line_buffering=True)
        sys.stderr.reconfigure(line_buffering=True)
    except Exception:
        pass
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
        stream=sys.stderr,
        force=True,
    )


def _install_watchdog():
    """Global wall-clock limit. Only available on POSIX (Linux — the Railway runtime)."""
    if not hasattr(signal, 'SIGALRM'):
        log.warning('watchdog unavailable on this platform (no SIGALRM)')
        return

    def _fire(signum, frame):
        log.error('WATCHDOG: run exceeded %ss during stage=%s — force exit', WATCHDOG_SECONDS, _current_stage)
        os._exit(2)

    signal.signal(signal.SIGALRM, _fire)
    signal.alarm(WATCHDOG_SECONDS)


class _Stage:
    """Context manager that logs start/end + elapsed and updates _current_stage."""
    def __init__(self, name):
        self.name = name
        self.t0 = 0.0

    def __enter__(self):
        global _current_stage
        _current_stage = self.name
        self.t0 = time.monotonic()
        log.info('stage=%s start', self.name)
        return self

    def __exit__(self, exc_type, exc, tb):
        dt = time.monotonic() - self.t0
        if exc_type is None:
            log.info('stage=%s done %.1fs', self.name, dt)
        else:
            log.exception('stage=%s failed after %.1fs: %s', self.name, dt, exc)
        return False  # never swallow


class Command(BaseCommand):
    help = 'Generate and send the weekly JB marketing report to Telegram'

    def handle(self, *args, **options):
        _configure_logging()
        _install_watchdog()
        log.info('marketing_report boot pid=%s python=%s', os.getpid(), sys.version.split()[0])

        # Deferred imports so a missing module here shows up as a normal stage failure
        # under the watchdog, not a bare ImportError at command-registration time.
        from website.marketing import (
            oauth, gsc, ga4, auditor, report, telegram,
            sitemap_checker, pagespeed, indexnow, omnihq_sync,
        )

        gsc_data = None
        ga4_data = None
        with _Stage('oauth_token'):
            token = oauth.get_access_token()
            if not token:
                log.warning('no google token — GSC + GA4 will be skipped this run')

        if token:
            with _Stage('gsc_fetch'):
                gsc_data = gsc.fetch_report(token)
                if gsc_data and 'error' in gsc_data:
                    log.warning('gsc returned error: %s', gsc_data['error'])
            with _Stage('ga4_fetch'):
                ga4_data = ga4.fetch_report(token)
                if ga4_data and 'error' in ga4_data:
                    log.warning('ga4 returned error: %s', ga4_data['error'])

        with _Stage('audit_pages'):
            audit_data = auditor.audit_pages()
            log.info('audit_pages returned %d entries', len(audit_data or []))

        with _Stage('sitemap_check'):
            sitemap_data = sitemap_checker.check_sitemap()
            if sitemap_data and 'error' in sitemap_data:
                log.warning('sitemap returned error: %s', sitemap_data['error'])
            elif sitemap_data:
                log.info('sitemap: %d URLs, %d ok, %d 404, %d timed_out',
                         sitemap_data.get('total', 0),
                         sitemap_data.get('ok', 0),
                         len(sitemap_data.get('not_found', [])),
                         sitemap_data.get('timed_out', 0))

        with _Stage('pagespeed'):
            speed_data = pagespeed.check_speed()
            log.info('pagespeed returned %d entries', len(speed_data or []))

        with _Stage('build_report'):
            message = report.build(gsc_data, ga4_data, audit_data, sitemap_data, speed_data)

        with _Stage('telegram_send'):
            ok = telegram.send(message, timeout=10)
            if not ok:
                log.error('telegram send failed — see stage exception above')
                # Cancel watchdog before exit so a slow atexit path doesn't collide
                if hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)
                sys.exit(1)

        with _Stage('omnihq_sync'):
            result = omnihq_sync.post_report(gsc_data, ga4_data, audit_data, sitemap_data, speed_data)
            log.info('omnihq_sync: %s', result)

        with _Stage('indexnow_ping'):
            pinged = indexnow.ping()
            log.info('indexnow: %s', 'ok' if pinged else 'failed (non-critical)')

        # Disarm watchdog on clean exit
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)
        log.info('marketing_report done')
