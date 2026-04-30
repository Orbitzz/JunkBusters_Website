"""Google Analytics 4 Data API client — sessions and conversions by page."""
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
        curr_data = query({
            'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
            'dimensions': [{'name': 'pagePath'}],
            'metrics': [{'name': 'sessions'}, {'name': 'conversions'}],
            'limit': 25,
        })

        prior_data = query({
            'dateRanges': [{'startDate': '14daysAgo', 'endDate': '8daysAgo'}],
            'dimensions': [{'name': 'pagePath'}],
            'metrics': [{'name': 'sessions'}],
            'limit': 25,
        })

        curr_pages = [
            {
                'page': row['dimensionValues'][0]['value'],
                'sessions': int(row['metricValues'][0]['value']),
                'conversions': int(row['metricValues'][1]['value']),
            }
            for row in curr_data.get('rows', [])
        ]

        curr_total = sum(p['sessions'] for p in curr_pages)
        prior_total = sum(
            int(row['metricValues'][0]['value'])
            for row in prior_data.get('rows', [])
        )
        session_delta = (
            round((curr_total - prior_total) / prior_total * 100) if prior_total else 0
        )

        top_pages = sorted(curr_pages, key=lambda x: x['sessions'], reverse=True)[:5]
        top_converters = sorted(
            [p for p in curr_pages if p['conversions'] > 0],
            key=lambda x: x['conversions'],
            reverse=True,
        )[:3]
        needs_cta = [
            p for p in curr_pages if p['sessions'] >= 30 and p['conversions'] == 0
        ][:3]

        return {
            'total_sessions': curr_total,
            'session_delta': session_delta,
            'top_pages': top_pages,
            'top_converters': top_converters,
            'needs_cta': needs_cta,
        }
    except Exception as e:
        return {'error': str(e)}
