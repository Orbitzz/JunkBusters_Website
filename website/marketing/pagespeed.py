"""Check Core Web Vitals via Google PageSpeed Insights API (no auth required)."""
import json
import urllib.request
import urllib.parse
import os

API_URL = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'

PAGES_TO_CHECK = [
    ('/', 'https://www.junkbustershauling.com/'),
    ('/junk-removal-nashville/', 'https://www.junkbustershauling.com/junk-removal-nashville/'),
    ('/estate-hoarder-cleanout/', 'https://www.junkbustershauling.com/estate-hoarder-cleanout/'),
]

_SCORE_LABEL = {range(0, 50): 'Poor', range(50, 90): 'Needs Work', range(90, 101): 'Good'}


def _label(score):
    for r, label in _SCORE_LABEL.items():
        if score in r:
            return label
    return ''


def check_speed():
    api_key = os.environ.get('PAGESPEED_API_KEY', '')
    results = []

    for slug, url in PAGES_TO_CHECK:
        try:
            params = {'url': url, 'strategy': 'mobile', 'category': 'performance'}
            if api_key:
                params['key'] = api_key
            req = urllib.request.Request(f'{API_URL}?{urllib.parse.urlencode(params)}')
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())

            cats = data.get('lighthouseResult', {}).get('categories', {})
            audits = data.get('lighthouseResult', {}).get('audits', {})
            score = round((cats.get('performance', {}).get('score') or 0) * 100)
            lcp = audits.get('largest-contentful-paint', {}).get('displayValue', 'N/A')
            fid = audits.get('total-blocking-time', {}).get('displayValue', 'N/A')
            cls = audits.get('cumulative-layout-shift', {}).get('displayValue', 'N/A')

            results.append({
                'slug': slug,
                'score': score,
                'label': _label(score),
                'lcp': lcp,
                'tbt': fid,
                'cls': cls,
            })
        except Exception as e:
            results.append({'slug': slug, 'error': str(e)})

    return results
