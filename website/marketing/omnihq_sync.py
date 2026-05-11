import json
import os
import urllib.request

WEBHOOK_URL = os.environ.get('OMNIHQ_REPORT_WEBHOOK_URL', '')
REPORT_TOKEN = os.environ.get('OMNIHQ_REPORT_TOKEN', '')


def post_report(gsc_data, ga4_data, audit_data, sitemap_data, speed_data,
                period_start=None, period_end=None):
    """POST marketing report data to OmniHQ. Fails silently if not configured."""
    if not WEBHOOK_URL or not REPORT_TOKEN:
        return False
    payload = json.dumps({
        'period_start': str(period_start) if period_start else None,
        'period_end': str(period_end) if period_end else None,
        'gsc_data': gsc_data or {},
        'ga4_data': ga4_data or {},
        'audit_data': audit_data or [],
        'sitemap_data': sitemap_data or {},
        'speed_data': speed_data or [],
    }).encode()
    try:
        req = urllib.request.Request(
            WEBHOOK_URL,
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'X-Report-Token': REPORT_TOKEN,
            },
        )
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception:
        return False
