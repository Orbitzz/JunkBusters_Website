"""Google Analytics 4 Data API client — sessions, conversions, engagement."""
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
        # Per-page: sessions + conversions (current week)
        curr_data = query({
            'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
            'dimensions': [{'name': 'pagePath'}],
            'metrics': [{'name': 'sessions'}, {'name': 'conversions'}],
            'limit': 25,
        })

        # Per-page: sessions (prior week, for delta)
        prior_data = query({
            'dateRanges': [{'startDate': '14daysAgo', 'endDate': '8daysAgo'}],
            'dimensions': [{'name': 'pagePath'}],
            'metrics': [{'name': 'sessions'}],
            'limit': 25,
        })

        # Site-wide engagement metrics (no dimensions = totals)
        engagement_data = query({
            'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
            'metrics': [
                {'name': 'newUsers'},
                {'name': 'engagementRate'},
                {'name': 'averageSessionDuration'},
                {'name': 'screenPageViews'},
            ],
            'limit': 1,
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

        # Parse site-wide engagement
        eng_row = (engagement_data.get('rows') or [{}])[0]
        eng_vals = eng_row.get('metricValues', [])
        new_users = int(eng_vals[0]['value']) if len(eng_vals) > 0 else 0
        engagement_rate = round(float(eng_vals[1]['value']) * 100) if len(eng_vals) > 1 else 0
        avg_duration = round(float(eng_vals[2]['value'])) if len(eng_vals) > 2 else 0
        page_views = int(eng_vals[3]['value']) if len(eng_vals) > 3 else 0

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
            'new_users': new_users,
            'engagement_rate': engagement_rate,
            'avg_duration': avg_duration,
            'page_views': page_views,
            'top_pages': top_pages,
            'top_converters': top_converters,
            'needs_cta': needs_cta,
        }
    except Exception as e:
        return {'error': str(e)}
