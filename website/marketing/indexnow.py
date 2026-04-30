"""Ping Bing IndexNow so new and updated pages get crawled within hours."""
import json
import os
import urllib.request
import urllib.error

INDEXNOW_API = 'https://api.indexnow.org/indexnow'
SITE_BASE = 'https://www.junkbustershauling.com'


def ping(urls=None):
    """
    Submit URLs to IndexNow. If urls is None, submits the sitemap page list.
    Returns True on success.
    """
    key = os.environ.get('INDEXNOW_KEY', 'jb2026indexnow8812ab4c9d3e7f1a')
    key_location = f'{SITE_BASE}/{key}.txt'

    if urls is None:
        urls = _default_urls()

    urls = [u if u.startswith('http') else f'{SITE_BASE}{u}' for u in urls]

    body = json.dumps({
        'host': 'www.junkbustershauling.com',
        'key': key,
        'keyLocation': key_location,
        'urlList': urls[:100],
    }).encode()

    try:
        req = urllib.request.Request(INDEXNOW_API, data=body, method='POST')
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status in (200, 202)
    except urllib.error.HTTPError as e:
        return e.code in (200, 202)
    except Exception:
        return False


def _default_urls():
    return [
        '/',
        '/junk-removal/',
        '/junk-removal-nashville/',
        '/junk-removal-clarksville/',
        '/junk-removal-bowling-green/',
        '/estate-hoarder-cleanout/',
        '/eviction-clean-out/',
        '/estate-clean-out/',
        '/foreclosure-clean-out/',
        '/storage-unit-clean-out/',
        '/hot-tub-removal/',
        '/garage-clean-out/',
        '/light-demolition/',
        '/scrap-metal-pickup/',
        '/dump-trailer-rental/',
        '/property-manager-hub/',
        '/short-term-rental-turnover/',
        '/move-out-deep-cleaning/',
        '/services/',
        '/areas-we-serve/',
        '/pricing/',
        '/faq/',
        '/llms.txt',
    ]
