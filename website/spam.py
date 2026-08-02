"""Bot / spam controls for lead-form endpoints."""
import json
import logging
import re
import urllib.parse
import urllib.request
from django.conf import settings
from django.core.cache import cache

log = logging.getLogger(__name__)

_TURNSTILE_URL = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'


# ── Regex primitives ─────────────────────────────────────────────────────────
_URL_RE = re.compile(r'(https?://|www\.|\.ru/|\.cn/|\.tk/|bit\.ly/)', re.I)

# Explicit non-Latin script blocks — deliberately excludes Latin Extended,
# smart quotes, curly apostrophes, em dashes, and other punctuation that
# mobile keyboards insert automatically.
_FOREIGN_SCRIPT_RE = re.compile(
    '['
    'Ѐ-ӿ'    # Cyrillic
    'Ԁ-ԯ'    # Cyrillic Supplement
    'Ͱ-Ͽ'    # Greek and Coptic
    '֐-׿'    # Hebrew
    '؀-ۿ'    # Arabic
    'ݐ-ݿ'    # Arabic Supplement
    'ऀ-ॿ'    # Devanagari
    '฀-๿'    # Thai
    '぀-ゟ'    # Hiragana
    '゠-ヿ'    # Katakana
    '一-鿿'    # CJK Unified Ideographs
    '가-힯'    # Hangul Syllables
    ']'
)

_DIGITS_RE = re.compile(r'\D+')

# Random-key bot signature — long unbroken run of caps with no vowels-then-consonants variation.
_ALLCAPS_JUNK_RE = re.compile(r'^[A-Z]{20,}$')


# Curated list keyed to spam actually observed in this inbox.
SPAM_KEYWORDS = (
    'xevil',
    'xevil 5.0',
    'xevil 6.0',
    'xevil 7.0',
    'xrumer',
    'recaptcha',
    'hcaptcha',
    'turnstile',
    'solve captcha',
    'captcha solving',
    'anti-captcha',
    '2captcha',
    'deathbycaptcha',
    'rucaptcha',
    'solvemedia',
    'bitcoinfaucet',
    'smm',
    'backlink',
    'guest post',
    'link building',
    'bitcoin',
    'forex',
    'casino',
    'pornhub',
    'viagra',
    'investment opportunity',
)


# ── Public helpers ───────────────────────────────────────────────────────────

def check_honeypot(request, field_names=('website_url', 'company_website')):
    """Return True if any hidden honeypot field arrived populated (bot signature)."""
    return any(request.POST.get(f, '') for f in field_names)


def _is_na_phone(phone):
    """North American Numbering Plan: 10 digits, or 11 starting with 1. Empty = not a signal."""
    if not phone:
        return True
    digits = _DIGITS_RE.sub('', phone)
    return len(digits) == 10 or (len(digits) == 11 and digits.startswith('1'))


def is_spam(name='', phone='', email='', message='', **_ignored):
    """Return (flagged: bool, reasons: list[str]). Short-circuits at first match."""
    reasons = []
    haystack = f'{name} {message}'.lower()

    if _URL_RE.search(message or ''):
        reasons.append('url_in_message')
    if _FOREIGN_SCRIPT_RE.search(name or '') or _FOREIGN_SCRIPT_RE.search(message or ''):
        reasons.append('foreign_script')
    if not _is_na_phone(phone):
        reasons.append('non_na_phone')
    if _ALLCAPS_JUNK_RE.match((name or '').replace(' ', '')):
        reasons.append('allcaps_name')
    for kw in SPAM_KEYWORDS:
        if kw in haystack:
            reasons.append(f'keyword:{kw}')
            break

    return (bool(reasons), reasons)


def get_client_ip(request):
    """Return the true visitor IP behind Cloudflare / any reverse proxy.

    Order:
      1. CF-Connecting-IP (Cloudflare, always the true origin if the request came through CF)
      2. Leftmost X-Forwarded-For entry (generic proxy convention)
      3. REMOTE_ADDR (direct-hit fallback)

    Note: none of these headers are cryptographically bound to Cloudflare.
    A request that bypasses Cloudflare and hits Railway directly could spoof
    CF-Connecting-IP. The worst case is that rate-limiter accounting is
    fooled — which was the pre-change state anyway, so net-neutral. Locking
    the origin to Cloudflare IP ranges is the proper hardening; out of scope here.
    """
    cf = request.META.get('HTTP_CF_CONNECTING_IP', '').strip()
    if cf:
        return cf
    xff = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '') or 'unknown'


def rate_limit_ok(request, key_prefix, limit=5, window=3600):
    """Per-IP fixed-window rate limit backed by Django cache.

    Called BEFORE spam scoring, so it counts every submission — clean and flagged
    alike. That's intentional: a bot cannot get unlimited flagged attempts.

    Returns True if the request is under the limit and the counter has been incremented.
    False if the caller is over-limit.

    Note: default Django cache is LocMemCache — per-worker on Gunicorn, so with 2 workers
    the effective ceiling is 2*limit per IP per window. Adequate as a coarse control.
    """
    ip = get_client_ip(request)
    key = f'{key_prefix}:{ip}'
    count = cache.get(key, 0)
    if count >= limit:
        return False
    cache.set(key, count + 1, window)
    return True


def notify_spam_flag(row):
    """Fire-and-forget Telegram alert when a submission is flagged.

    Runs inline on submission so the review loop does not depend on the marketing
    cron (which has its own independent outage). Uses the existing Telegram bot;
    routes to the same channel as the marketing report.

    Failure is logged, never raised — a Telegram outage must not break lead intake.
    """
    try:
        from website.marketing import telegram
        snippet = (row.notes or '')[:100].replace('\n', ' ').strip()
        if len(row.notes or '') > 100:
            snippet += '…'
        msg = (
            '<b>Spam-flagged submission</b>\n'
            f'{row.first_name} {row.last_name} — {row.phone or "no phone"}\n'
            f'form: {row.service_requested[:60]}\n'
            f'reasons: <i>{row.spam_reasons or "(none recorded)"}</i>\n'
            f'msg: {snippet}\n'
            '<i>Check Django admin if this is a real lead.</i>'
        )
        # 3s cap — this send sits in the request path; a false-positive flag must
        # not stall a real customer's response.
        telegram.send(msg, timeout=3)
    except Exception:
        log.exception('spam: telegram notify failed')


def notify_lead(row):
    """Inline Telegram alert for a real (non-flagged) submission.

    Runs alongside the email notification so leads reach a channel Christian
    actually reads, without waiting on the marketing cron. Email stays as
    a backup — this is additive, not a replacement.
    """
    try:
        from website.marketing import telegram
        snippet = (row.notes or '')[:200].replace('\n', ' ').strip()
        if len(row.notes or '') > 200:
            snippet += '…'
        # Distinct header + emoji-free formatting; Christian is scanning the same
        # channel for spam-digest and lead alerts, so make the difference obvious.
        msg = (
            '<b>NEW LEAD</b>\n'
            f'<b>{row.first_name} {row.last_name}</b>\n'
            f'phone: <a href="tel:{row.phone}">{row.phone}</a>\n'
            f'email: {row.email}\n'
            f'form: {row.service_requested[:80]}\n'
            f'msg: {snippet}'
        )
        telegram.send(msg, timeout=3)
    except Exception:
        log.exception('lead: telegram notify failed')


# ── Turnstile ────────────────────────────────────────────────────────────────

def verify_turnstile(request):
    """Verify a Cloudflare Turnstile token against Cloudflare's siteverify endpoint.

    Fail-open when TURNSTILE_SECRET_KEY is unset (misconfig-safe during rollout).
    Set TURNSTILE_REQUIRED=True on Railway once the widget is confirmed working
    to switch to fail-closed on missing/invalid tokens.

    Token arrives in POST as 'cf-turnstile-response' for form submits, or under
    'cf_turnstile_response' inside the JSON body for the chat proxy.
    """
    secret = getattr(settings, 'TURNSTILE_SECRET_KEY', '')
    required = getattr(settings, 'TURNSTILE_REQUIRED', False)

    if not secret:
        if required:
            log.error('TURNSTILE_SECRET_KEY missing and TURNSTILE_REQUIRED=True — blocking submission')
            return False
        # Fail-open: intentional during rollout so a missing key does not drop leads.
        return True

    token = request.POST.get('cf-turnstile-response', '')
    if not token and request.content_type and 'json' in request.content_type:
        try:
            token = (json.loads(request.body or b'{}').get('cf_turnstile_response') or '')
        except Exception:
            token = ''

    if not token:
        log.warning('Turnstile: no token in request')
        return not required

    body = urllib.parse.urlencode({
        'secret': secret,
        'response': token,
        'remoteip': get_client_ip(request),
    }).encode()
    try:
        req = urllib.request.Request(_TURNSTILE_URL, data=body, method='POST')
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        if data.get('success'):
            return True
        log.warning('Turnstile: verify failed — %s', data.get('error-codes'))
        return False
    except Exception as e:
        log.exception('Turnstile: verify exception %s', e)
        # Network hiccups should not drop real leads unless strictly required.
        return not required
