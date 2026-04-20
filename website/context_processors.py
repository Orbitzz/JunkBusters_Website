from pathlib import Path
from django.conf import settings

GOOGLE_REVIEW_URL = getattr(settings, 'GOOGLE_REVIEW_URL', 'https://g.page/r/CaQvxFrtKJyzEBM/review')
QR_CODE_PATH = Path(settings.BASE_DIR) / 'static' / 'img' / 'Google Review QR.png'
LOGO_PATH = Path(settings.BASE_DIR) / 'static' / 'img' / 'logo.png'

FC_REVIEWS_URL = settings.FIELDCOMMAND_REVIEWS_URL
FC_API_KEY     = settings.FIELDCOMMAND_EMBED_API_KEY


def _fetch_fc_reviews():
    """Try FieldCommand widget API. Returns list of raw FC review dicts or None."""
    try:
        import urllib.request, json
        req = urllib.request.Request(
            FC_REVIEWS_URL,
            headers={'X-FC-EMBED-KEY': FC_API_KEY}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read())
        if data.get('success') and data.get('reviews'):
            return data['reviews']
    except Exception:
        pass
    return None


def _map_fc_reviews(fc_reviews):
    """Map FieldCommand fields to the shape _reviews.html expects."""
    from .google_reviews import _relative_time
    out = []
    for r in fc_reviews:
        out.append({
            'author_name':       r.get('name', 'Customer'),
            'rating':            r.get('rating', 5),
            'text':              r.get('comment', ''),
            'relative_time':     _relative_time(r.get('created_at', '')),
            'profile_photo_url': '',
        })
    return out


def google_reviews(request):
    """Inject reviews into every template context — FieldCommand first, then fallback."""
    from .google_reviews import get_reviews, get_summary

    fc_raw = _fetch_fc_reviews()
    if fc_raw:
        reviews = _map_fc_reviews(fc_raw)
        is_live = True
    else:
        reviews, is_live = get_reviews()  # GBP OAuth / Places API / static fallback

    summary = get_summary()
    return {
        'google_reviews':      reviews,
        'google_reviews_live': is_live,
        'google_summary':      summary,
        'review_url':          GOOGLE_REVIEW_URL,
        'qr_code_exists':      QR_CODE_PATH.exists(),
    }


def business_info(request):
    return {
        'BUSINESS_NAME': getattr(settings, 'BUSINESS_NAME', 'Junk Busters Hauling & Junk Removal'),
        'BUSINESS_PHONE': getattr(settings, 'BUSINESS_PHONE', '615-881-2505'),
        'BUSINESS_EMAIL': getattr(settings, 'BUSINESS_EMAIL', 'info@junkbustershauling.com'),
        'BUSINESS_ADDRESS': getattr(settings, 'BUSINESS_ADDRESS', 'White House & Nashville, Tennessee'),
        'GOOGLE_REVIEW_URL': GOOGLE_REVIEW_URL,
        'qr_code_exists': QR_CODE_PATH.exists(),
        'nav_logo_exists': LOGO_PATH.exists(),
    }
