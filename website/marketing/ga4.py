"""Google Analytics 4 Data API client — sessions and key events by page."""
import json
import os
import urllib.request


def fetch_report(access_token):
    property_id = os.environ.get('GA4_PROPERTY_ID', '')
    if not property_id or not access_token:
        return None

    url = f'https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport'

    def query(body_dict):
        body = json.dumps(body_dict).encode()
        req = urllib.request.Request(url, data=body, method='POST')
        req.add_header('Authorization', f'Bearer {access_token}')
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())

    try:
        # Pages by sessions — current 7 days and prior 7 days as separate dateRange dimension
        data = query({
            'dateRanges': [
                {'startDate': '7daysAgo', 'endDate': 'today', 'name': 'current'},
                {'startDate': '14daysAgo', 'endDate': '8daysAgo', 'name': 'prior'},
            ],
            'dimensions': [{'name': 'pagePath'}, {'name': 'dateRange'}],
            'metrics': [{'name': 'sessions'}, {'name': 'keyEvents'}],
            'limit': 50,
            'orderBys': [{'metric': {'metricName': 'sessions'}, 'desc': True}],
        })

        curr = {}
        prior_sessions = {}
        for row in data.get('rows', []):
            page = row['dimensionValues'][0]['value']
            range_name = row['dimensionValues'][1]['value']
            sessions = int(row['metricValues'][0]['value'])
            key_events = int(row['metricValues'][1]['value'])
            if range_name == 'current':
                curr[page] = {'sessions': sessions, 'key_events': key_events}
            else:
                prior_sessions[page] = sessions

        total_curr = sum(v['sessions'] for v in curr.values())
        total_prior = sum(prior_sessions.values())
        session_delta = (
            round((total_curr - total_prior) / total_prior * 100) if total_prior else 0
        )

        pages = [{'page': p, **v} for p, v in curr.items()]
        top_pages = sorted(pages, key=lambda x: x['sessions'], reverse=True)[:5]
        top_converters = sorted(
            [p for p in pages if p['key_events'] > 0],
            key=lambda x: x['key_events'],
            reverse=True,
        )[:3]
        needs_cta = [p for p in pages if p['sessions'] >= 30 and p['key_events'] == 0][:3]

        return {
            'total_sessions': total_curr,
            'session_delta': session_delta,
            'top_pages': top_pages,
            'top_converters': top_converters,
            'needs_cta': needs_cta,
        }
    except Exception as e:
        return {'error': str(e)}
