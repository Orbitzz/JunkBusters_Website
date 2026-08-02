"""Fetch live sitemap.xml and check every URL for 200/301/404 in parallel."""
import urllib.request
import urllib.error
from xml.etree import ElementTree
import concurrent.futures

SITEMAP_URL = 'https://www.junkbustershauling.com/sitemap.xml'
_UA = {'User-Agent': 'JBMarketingBot/1.0'}

# Per-request and total wall-clock caps. Sitemap covers ~50 URLs; if the crawl
# stalls (dead upstream, DNS meltdown), the total budget kicks in so the cron
# stage cannot hang the entire job.
_PER_REQUEST_TIMEOUT = 10
_TOTAL_BUDGET_SECONDS = 90


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def _check_url(url):
    try:
        req = urllib.request.Request(url, method='HEAD', headers=_UA)
        opener = urllib.request.build_opener(_NoRedirect())
        with opener.open(req, timeout=_PER_REQUEST_TIMEOUT) as resp:
            return url, resp.status
    except urllib.error.HTTPError as e:
        return url, e.code
    except Exception:
        return url, 0


def check_sitemap():
    try:
        req = urllib.request.Request(SITEMAP_URL, headers=_UA)
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml = resp.read()
    except Exception as e:
        return {'error': str(e)}

    try:
        root = ElementTree.fromstring(xml)
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text.strip() for loc in root.findall('.//sm:loc', ns) if loc.text]
    except Exception as e:
        return {'error': f'XML parse failed: {e}'}

    urls = urls[:80]

    results = []
    timed_out_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(_check_url, u): u for u in urls}
        done, not_done = concurrent.futures.wait(
            futures.keys(),
            timeout=_TOTAL_BUDGET_SECONDS,
            return_when=concurrent.futures.ALL_COMPLETED,
        )
        for fut in done:
            try:
                results.append(fut.result(timeout=0))
            except Exception:
                results.append((futures[fut], 0))
        for fut in not_done:
            fut.cancel()
            timed_out_count += 1

    ok, redirects, not_found, errors = [], [], [], []
    for url, code in results:
        if code == 200:
            ok.append(url)
        elif code in (301, 302, 308):
            redirects.append(url)
        elif code == 404:
            not_found.append(url)
        else:
            errors.append({'url': url, 'code': code})

    return {
        'total': len(urls),
        'ok': len(ok),
        'redirects': redirects,
        'not_found': not_found,
        'errors': errors,
        'timed_out': timed_out_count,
    }
