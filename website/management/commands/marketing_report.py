import sys
from django.core.management.base import BaseCommand
from website.marketing import oauth, gsc, ga4, auditor, report, telegram, sitemap_checker, pagespeed


class Command(BaseCommand):
    help = 'Generate and send the weekly JB marketing report to Telegram'

    def handle(self, *args, **options):
        self.stdout.write('Getting Google access token...')
        token = oauth.get_access_token()

        if token:
            self.stdout.write('Fetching GSC data...')
            gsc_data = gsc.fetch_report(token)
            self.stdout.write('Fetching GA4 data...')
            ga4_data = ga4.fetch_report(token)
        else:
            self.stdout.write(self.style.WARNING(
                'No Google credentials — sending audit only. '
                'Run /marketing-auth/start/ to authorize GSC + GA4.'
            ))
            gsc_data = None
            ga4_data = None

        self.stdout.write('Auditing site pages...')
        audit_data = auditor.audit_pages()

        self.stdout.write('Checking sitemap health...')
        sitemap_data = sitemap_checker.check_sitemap()

        self.stdout.write('Checking page speed...')
        speed_data = pagespeed.check_speed()

        self.stdout.write('Building report...')
        message = report.build(gsc_data, ga4_data, audit_data, sitemap_data, speed_data)

        self.stdout.write('Sending to Telegram...')
        ok = telegram.send(message)

        if ok:
            self.stdout.write(self.style.SUCCESS('Report sent successfully'))
        else:
            self.stdout.write(self.style.ERROR('Failed to send report'))
            sys.exit(1)
