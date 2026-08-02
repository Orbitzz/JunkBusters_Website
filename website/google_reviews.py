"""
Fetch live Google reviews.

Priority order:
  1. Google Business Profile API (OAuth2) — returns ALL reviews AND accurate total count
  2. OmniHQ widget API — fallback, returns whatever OmniHQ has cached
  3. Google Places API — fallback, returns max 5 reviews + user_ratings_total (if key is unrestricted)
  4. Static fallback reviews

Refresh token resolution: prefer env var GOOGLE_REVIEWS_REFRESH_TOKEN
(survives redeploys), fall back to _oauth_tokens.json (local dev).
"""
import json
import os
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from django.conf import settings

CACHE_FILE = Path(__file__).parent / '_google_reviews_cache.json'
TOKEN_FILE = Path(__file__).parent / '_oauth_tokens.json'
IDS_FILE   = Path(__file__).parent / '_gbp_ids.json'  # long-lived account/location IDs
CACHE_TTL  = 86400  # 24 hours

FALLBACK_REVIEWS = [
    {
        'author_name': 'Jennifer B.',
        'rating': 5,
        'text': "They were great! Moved everything out quickly and would absolutely use them again! I called them a couple of days ago for the 2nd time and they came this morning! They are great to work with so nice and kind! I know who I will be calling next time!",
        'relative_time': 'recently',
        'profile_photo_url': '',
    },
    {
        'author_name': 'Shelby H.',
        'rating': 5,
        'text': "I am so glad we hired Junk Busters to come help us and clean up our yard. Christian was very responsive, professional, and scheduled to come take care of it in 24 hours. He seriously did such a great job in the awful heat of July. I cannot recommend him enough!",
        'relative_time': '1 month ago',
        'profile_photo_url': '',
    },
    {
        'author_name': 'Claire W.',
        'rating': 5,
        'text': "Christian and his team at Junk Busters were quick, professional, and so nice! I gave out their info to two other friends who plan to book them as well! Absolutely would recommend them to anyone who needs to get rid of old junk, big or small.",
        'relative_time': '3 weeks ago',
        'profile_photo_url': '',
    },
    {
        'author_name': 'Leslie D.',
        'rating': 5,
        'text': "Needed a shed cleaned out and Christian and his wife did an amazing job! They were very thorough and got the job done quickly and painlessly! Would definitely use them again if needed!",
        'relative_time': '2 months ago',
        'profile_photo_url': '',
    },
]


# ── Token helpers ──────────────────────────────────────────────────────────────

def _load_tokens():
    """Resolve the refresh token in this order:
       1. Env var GOOGLE_REVIEWS_REFRESH_TOKEN (survives Railway redeploys — preferred)
       2. _oauth_tokens.json on the container filesystem (for local dev / one-off backfill)
    Access-token cache lives in-memory only; refresh happens each hour when Google's
    ~1-hour access token expires."""
    env_refresh = os.environ.get('GOOGLE_REVIEWS_REFRESH_TOKEN', '').strip()
    if env_refresh:
        return {'refresh_token': env_refresh, 'access_token': '', 'expires_at': 0}
    try:
        if TOKEN_FILE.exists():
            return json.loads(TOKEN_FILE.read_text())
    except Exception:
        pass
    return None


def _save_tokens(tokens):
    """Persist tokens to disk. No-op when using the env-var path (nowhere to persist
    an in-memory access token; refresh happens per-request when cache expires)."""
    try:
        TOKEN_FILE.write_text(json.dumps(tokens))
    except Exception:
        pass


def _refresh_access_token(tokens):
    """Exchange refresh_token for a new access_token. Returns updated tokens dict or None."""
    client_id = getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', '')
    client_secret = getattr(settings, 'GOOGLE_OAUTH_CLIENT_SECRET', '')
    if not client_id or not client_secret or not tokens.get('refresh_token'):
        return None
    try:
        body = urllib.parse.urlencode({
            'grant_type': 'refresh_token',
            'refresh_token': tokens['refresh_token'],
            'client_id': client_id,
            'client_secret': client_secret,
        }).encode()
        req = urllib.request.Request('https://oauth2.googleapis.com/token', data=body, method='POST')
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        tokens['access_token'] = data['access_token']
        tokens['expires_at'] = time.time() + data.get('expires_in', 3600) - 60
        _save_tokens(tokens)
        return tokens
    except Exception:
        return None


def get_valid_access_token():
    """Return a valid access token, refreshing if needed. Returns None if no tokens stored."""
    tokens = _load_tokens()
    if not tokens:
        return None
    if time.time() < tokens.get('expires_at', 0):
        return tokens['access_token']
    refreshed = _refresh_access_token(tokens)
    return refreshed['access_token'] if refreshed else None


# ── Cache helpers ──────────────────────────────────────────────────────────────

def _load_cache():
    try:
        if CACHE_FILE.exists():
            data = json.loads(CACHE_FILE.read_text())
            if time.time() - data.get('fetched_at', 0) < CACHE_TTL:
                return data
    except Exception:
        pass
    return None


def _save_cache(reviews, summary):
    try:
        CACHE_FILE.write_text(json.dumps({
            'fetched_at': time.time(),
            'reviews': reviews,
            'summary': summary,
        }))
    except Exception:
        pass


# ── Business Profile API ───────────────────────────────────────────────────────

def _api_get(url, access_token):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {access_token}'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def _load_ids():
    try:
        if IDS_FILE.exists():
            d = json.loads(IDS_FILE.read_text())
            if d.get('account_name') and d.get('location_name'):
                return d['account_name'], d['location_name']
    except Exception:
        pass
    return None, None


def _save_ids(account_name, location_name):
    try:
        IDS_FILE.write_text(json.dumps({'account_name': account_name, 'location_name': location_name}))
    except Exception:
        pass


def _fetch_business_profile_reviews(access_token):
    """
    Fetch reviews from Google Business Profile API.
    Returns (reviews_list, summary_dict) or (None, None) on failure.

    Account and location IDs are cached permanently in _gbp_ids.json — the
    /v1/accounts and /v1/{account}/locations endpoints are rate-limited to
    ~1 request per minute and the identifiers never change. Only the reviews
    pagination runs per fetch, which has a much higher quota.
    """
    try:
        account_name, location_name = _load_ids()
        if not account_name or not location_name:
            # First-time lookup: fetch and cache identifiers.
            accounts_data = _api_get(
                'https://mybusinessaccountmanagement.googleapis.com/v1/accounts',
                access_token,
            )
            accounts = accounts_data.get('accounts', [])
            if not accounts:
                return None, None
            account_name = accounts[0]['name']

            locations_data = _api_get(
                f'https://mybusinessinformation.googleapis.com/v1/{account_name}/locations'
                '?readMask=name,title,storefrontAddress',
                access_token,
            )
            locations = locations_data.get('locations', [])
            if not locations:
                return None, None
            location_name = locations[0]['name']
            _save_ids(account_name, location_name)

        # Step 3: fetch reviews (paginated). pageSize=50 is the API max; ceiling of
        # 10 pages covers up to 500 reviews. Prior version capped at 5×10=50 and
        # relied on the Places API for the total count — Places has been returning
        # REQUEST_DENIED for referrer-restricted keys, so the summary was falling
        # through to a hardcoded 160. len(all_reviews) after full pagination IS
        # the actual live total from Google Business Profile.
        all_reviews = []
        api_total = None
        page_token = None
        for _ in range(10):
            url = (
                f'https://mybusinessreviews.googleapis.com/v1/{account_name}/{location_name}/reviews'
                '?pageSize=50'
            )
            if page_token:
                url += f'&pageToken={page_token}'
            reviews_data = _api_get(url, access_token)
            if api_total is None and 'totalReviewCount' in reviews_data:
                api_total = int(reviews_data.get('totalReviewCount') or 0)
            batch = reviews_data.get('reviews', [])
            for r in batch:
                reviewer = r.get('reviewer', {})
                comment = r.get('comment', '')
                star = r.get('starRating', 'FIVE')
                star_map = {'ONE': 1, 'TWO': 2, 'THREE': 3, 'FOUR': 4, 'FIVE': 5}
                rating = star_map.get(star, 5)
                create_time = r.get('createTime', '')
                relative = _relative_time(create_time)
                all_reviews.append({
                    'author_name': reviewer.get('displayName', 'Customer'),
                    'rating': rating,
                    'text': comment,
                    'relative_time': relative,
                    'profile_photo_url': reviewer.get('profilePhotoUrl', ''),
                })
            page_token = reviews_data.get('nextPageToken')
            if not page_token:
                break

        # Step 4: summary. Prefer the API's totalReviewCount when present, otherwise
        # use len(all_reviews) — either way, no dependency on Places API for the total.
        avg_rating = (sum(r['rating'] for r in all_reviews) / len(all_reviews)) if all_reviews else 5.0
        total = api_total if api_total else len(all_reviews)
        summary = {'rating': round(avg_rating, 1), 'total': total}

        return all_reviews, summary
    except Exception:
        return None, None


def _relative_time(iso_str):
    """Convert ISO 8601 timestamp to rough relative string."""
    if not iso_str:
        return 'recently'
    try:
        import re
        # Parse basic ISO: 2024-11-15T12:34:56Z
        m = re.match(r'(\d{4})-(\d{2})-(\d{2})', iso_str)
        if not m:
            return 'recently'
        import datetime
        review_date = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        today = datetime.date.today()
        days = (today - review_date).days
        if days < 7:
            return f'{days} day{"s" if days != 1 else ""} ago' if days > 0 else 'today'
        elif days < 30:
            weeks = days // 7
            return f'{weeks} week{"s" if weeks != 1 else ""} ago'
        elif days < 365:
            months = days // 30
            return f'{months} month{"s" if months != 1 else ""} ago'
        else:
            years = days // 365
            return f'{years} year{"s" if years != 1 else ""} ago'
    except Exception:
        return 'recently'


# ── Places API fallback ────────────────────────────────────────────────────────

def _fetch_places_reviews():
    """Fetch up to 5 reviews from Places API. Returns (reviews, summary) or (None, None)."""
    api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
    place_id = getattr(settings, 'GOOGLE_PLACE_ID', '')
    if not api_key or not place_id:
        return None, None
    try:
        url = (
            f'https://maps.googleapis.com/maps/api/place/details/json'
            f'?place_id={place_id}'
            f'&fields=name,rating,user_ratings_total,reviews'
            f'&reviews_sort=newest'
            f'&key={api_key}'
        )
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
        if data.get('status') == 'OK':
            result = data.get('result', {})
            reviews = [
                {
                    'author_name': r.get('author_name', ''),
                    'rating': r.get('rating', 5),
                    'text': r.get('text', ''),
                    'relative_time': r.get('relative_time_description', ''),
                    'profile_photo_url': r.get('profile_photo_url', ''),
                }
                for r in result.get('reviews', [])
            ]
            summary = {
                'rating': result.get('rating', 5.0),
                'total': result.get('user_ratings_total', 0),
            }
            return reviews, summary
    except Exception:
        pass
    return None, None


def get_summary_from_places():
    """Used internally to get total review count from Places API."""
    _, summary = _fetch_places_reviews()
    return summary or {'rating': 5.0, 'total': 160}


# ── OmniHQ reviews API ────────────────────────────────────────────────────────

def _fetch_omnihq_reviews():
    """
    Fetch reviews from OmniHQ's widget API (which pulls from GBP OAuth
    stored in OmniHQ, falling back to OmniHQ's internal review DB).
    Returns (reviews_list, None) or (None, None) on failure.
    """
    api_url = getattr(settings, 'OMNIHQ_REVIEWS_URL', '')
    api_key = getattr(settings, 'OMNIHQ_EMBED_API_KEY', '')
    if not api_url or not api_key:
        return None, None
    try:
        url = f'{api_url.rstrip("/")}/?key={urllib.parse.quote(api_key, safe="")}'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        if not data.get('success'):
            return None, None
        reviews = []
        for r in data.get('reviews') or []:
            reviews.append({
                'author_name': r.get('name') or 'Customer',
                'rating': int(r.get('rating') or 5),
                'text': r.get('comment') or '',
                'relative_time': _relative_time(r.get('created_at') or ''),
                'profile_photo_url': '',
            })
        return (reviews, None) if reviews else (None, None)
    except Exception:
        return None, None


# ── Public API ─────────────────────────────────────────────────────────────────

def get_reviews():
    """
    Return (reviews_list, is_live).
    Priority: Business Profile API → OmniHQ API → Places API → static fallback.
    GBP is first because it is the only source that returns an accurate
    total review count. Results cached for 24 hours.
    """
    cached = _load_cache()
    if cached is not None:
        return cached['reviews'], True

    # 1. GBP (via env-var refresh token or file-based token) — accurate total
    access_token = get_valid_access_token()
    if access_token:
        reviews, summary = _fetch_business_profile_reviews(access_token)
        if reviews:
            _save_cache(reviews, summary)
            return reviews, True

    # 2. Fall back to OmniHQ widget API — uses OmniHQ's own GBP OAuth
    reviews, _ = _fetch_omnihq_reviews()
    if reviews:
        summary = get_summary_from_places() or {'rating': 5.0, 'total': len(reviews)}
        _save_cache(reviews, summary)
        return reviews, True

    # 3. Fall back to Places API (max 5 reviews)
    reviews, summary = _fetch_places_reviews()
    if reviews:
        _save_cache(reviews, summary)
        return reviews, True

    return FALLBACK_REVIEWS, False


def get_summary():
    """Return {'rating': X, 'total': Y} — from cache, live GBP fetch, Places API, or fallback."""
    cached = _load_cache()
    if cached and cached.get('summary'):
        return cached['summary']
    # If we can hit GBP, that has the accurate total.
    access_token = get_valid_access_token()
    if access_token:
        reviews, summary = _fetch_business_profile_reviews(access_token)
        if summary:
            _save_cache(reviews or [], summary)
            return summary
    _, summary = _fetch_places_reviews()
    return summary or {'rating': 5.0, 'total': 160}
