"""Scrape live site pages and score content quality."""
import urllib.request
import urllib.error
import re
from html.parser import HTMLParser

SITE_BASE = 'https://junkbusterstn.com'

PRIORITY_PAGES = [
    '/estate-hoarder-cleanout/',
    '/eviction-clean-out/',
    '/estate-clean-out/',
    '/foreclosure-clean-out/',
    '/storage-unit-clean-out/',
    '/junk-removal-nashville/',
    '/junk-removal-clarksville/',
    '/junk-removal-bowling-green/',
    '/hot-tub-removal/',
    '/garage-clean-out/',
    '/shed-demolition/',
]

_SKIP_TAGS = {'script', 'style', 'noscript', 'head', 'nav', 'footer'}


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in _SKIP_TAGS:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in _SKIP_TAGS and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            stripped = data.strip()
            if stripped:
                self.parts.append(stripped)

    def text(self):
        return ' '.join(self.parts)


def _word_count(html):
    p = _TextExtractor()
    p.feed(html)
    words = [w for w in p.text().split() if len(w) > 2]
    return len(words)


def _faq_count(html):
    return html.count('<details')


def _has_faq_schema(html):
    return '"@type":"FAQPage"' in html or '"@type": "FAQPage"' in html


def _score(words, faqs, has_schema):
    if words < 300 or faqs == 0:
        return 'red'
    if words < 500 or not has_schema:
        return 'yellow'
    return 'green'


def audit_pages():
    results = []
    for slug in PRIORITY_PAGES:
        url = f'{SITE_BASE}{slug}'
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'JBMarketingBot/1.0'})
            with urllib.request.urlopen(req, timeout=12) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
            words = _word_count(html)
            faqs = _faq_count(html)
            has_schema = _has_faq_schema(html)
            results.append({
                'slug': slug,
                'words': words,
                'faqs': faqs,
                'has_schema': has_schema,
                'priority': _score(words, faqs, has_schema),
            })
        except Exception as e:
            results.append({'slug': slug, 'error': str(e), 'priority': 'red'})
    return results
