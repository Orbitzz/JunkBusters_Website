"""Bot / spam controls for lead-form endpoints.

Three primitives:
  - check_honeypot(request): True if any honeypot field is non-empty.
  - is_spam(name, phone, email, message): heuristic scorer, returns (flagged, reasons).
  - rate_limit_ok(request, key_prefix, limit, window): per-IP token bucket via Django cache.

Turnstile verification lives in verify_turnstile() and is wired up in a later rollout.
"""
import logging
import re
from django.core.cache import cache

log = logging.getLogger(__name__)


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


# ── Turnstile (wired up in the P1 rollout, not called from views yet) ────────

def verify_turnstile(request):
    """Placeholder — implemented and wired in Priority 1 rollout."""
    return True
