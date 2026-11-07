"""Shared headers for every request the website makes to OmniHQ.

Cloudflare in front of omnihq.io refuses Python's default "Python-urllib"
User-Agent with a 403 before the request reaches OmniHQ, so every call
must identify itself with a named User-Agent.
"""
USER_AGENT = 'JunkBustersWebsite/1.0 (+https://www.junkbustershauling.com)'


def ohq_headers(extra=None):
    headers = {'User-Agent': USER_AGENT}
    if extra:
        headers.update(extra)
    return headers
