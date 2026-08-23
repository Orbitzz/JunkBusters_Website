class UTMCaptureMiddleware:
    """Store UTM params + referrer in session on first landing so forms can include them."""
    UTM_PARAMS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if any(p in request.GET for p in self.UTM_PARAMS):
            for param in self.UTM_PARAMS:
                if param in request.GET:
                    request.session[param] = request.GET[param]
            request.session['utm_referrer'] = request.META.get('HTTP_REFERER', '')
        return self.get_response(request)


class NoindexInternalEndpointsMiddleware:
    """Stamp X-Robots-Tag: noindex on every response for internal JSON / AJAX /
    webhook endpoints. Belt-and-suspenders with the robots.txt Disallow lines
    for the same prefixes — robots.txt only prevents recrawl of currently
    unindexed URLs; the header removes anything already indexed on next crawl.
    Applies regardless of status code so 405s and 5xxs are covered too."""
    PREFIXES = ('/api/', '/gift-card/webhook/', '/portal/webhook/')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith(self.PREFIXES):
            response['X-Robots-Tag'] = 'noindex'
        return response
