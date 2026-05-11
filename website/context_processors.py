from pathlib import Path
from django.conf import settings

GOOGLE_REVIEW_URL = getattr(settings, 'GOOGLE_REVIEW_URL', 'https://g.page/r/CaQvxFrtKJyzEBM/review')
QR_CODE_PATH = Path(settings.BASE_DIR) / 'static' / 'img' / 'Google Review QR.png'
LOGO_PATH = Path(settings.BASE_DIR) / 'static' / 'img' / 'logo.png'

def google_reviews(request):
    """Inject reviews into every template context — 24-hour cached, OmniHQ → GBP → Places → static."""
    from .google_reviews import get_reviews, get_summary

    reviews, is_live = get_reviews()
    summary = get_summary()
    return {
        'google_reviews':      reviews,
        'google_reviews_live': is_live,
        'google_summary':      summary,
        'review_url':          GOOGLE_REVIEW_URL,
        'qr_code_exists':      QR_CODE_PATH.exists(),
    }


def customer_profile(request):
    """Inject the logged-in user's CustomerProfile into every template."""
    if request.user.is_authenticated:
        from portal.models import CustomerProfile
        profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
        return {'profile': profile}
    return {'profile': None}


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
