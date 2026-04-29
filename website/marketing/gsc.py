"""Google Search Console API client — last 7 days vs prior 7 days."""
import json
import os
import urllib.request
import urllib.parse
from datetime import date, timedelta


def fetch_report(access_token):
    site_url = os.environ.get('GSC_SITE_URL', '')
    if not site_url or not access_token:
        return None

    encoded = urllib.parse.quote(site_url, safe='')
    endpoint = f'https://www.googleapis.com/webmasters/v3/sites/{encoded}/searchAnalytics/query'

    # GSC data has a ~3-day processing delay
    today = date.today()
    end = today - timedelta(days=3)
    start = end - timedelta(days=6)
    prior_end = start - timedelta(days=1)
    prior_start = prior_end - timedelta(days=6)

    def query(start_d, end_d, dimensions, row_limit=25):
        body = json.dumps({
            'startDate': start_d.isoformat(),
            'endDate': end_d.isoformat(),
            'dimensions': dimensions,
            'rowLimit': row_limit,
        }).encode()
        req = urllib.request.Request(endpoint, data=body, method='POST')
        req.add_header('Authorization', f'Bearer {access_token}')
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read()).get('rows', [])

    try:
        curr_rows = query(start, end, ['query'], 25)
        prior_rows = query(prior_start, prior_end, ['query'], 25)
        curr_pages = query(start, end, ['page'], 20)
        prior_pages = query(prior_start, prior_end, ['page'], 20)

        prior_query_clicks = {r['keys'][0]: r['clicks'] for r in prior_rows}
        prior_page_clicks = {r['keys'][0]: r['clicks'] for r in prior_pages}

        top_queries = sorted(curr_rows, key=lambda r: r['clicks'], reverse=True)[:10]

        page2 = sorted(
            [r for r in curr_rows if 11 <= r.get('position', 0) <= 20],
            key=lambda r: r['impressions'],
            reverse=True,
        )[:5]

        declining = []
        for r in curr_pages:
            page = r['keys'][0]
            prev = prior_page_clicks.get(page, 0)
            curr = r['clicks']
            if prev > 2 and curr < prev * 0.8:
                pct = round((curr - prev) / prev * 100)
                declining.append({'page': page, 'clicks': curr, 'prev': prev, 'pct': pct})
        declining = sorted(declining, key=lambda x: x['pct'])[:3]

        total_clicks = sum(r['clicks'] for r in curr_rows)
        total_impressions = sum(r['impressions'] for r in curr_rows)
        prior_total = sum(r['clicks'] for r in prior_rows)
        click_delta = round((total_clicks - prior_total) / prior_total * 100) if prior_total else 0

        weighted_pos = sum(r['position'] * r['impressions'] for r in curr_rows)
        total_impr = sum(r['impressions'] for r in curr_rows)
        avg_position = round(weighted_pos / total_impr, 1) if total_impr else 0

        return {
            'total_clicks': total_clicks,
            'total_impressions': total_impressions,
            'avg_position': avg_position,
            'click_delta': click_delta,
            'top_queries': top_queries,
            'page2': page2,
            'declining': declining,
            'date_range': f'{start.isoformat()} → {end.isoformat()}',
        }
    except Exception as e:
        return {'error': str(e)}
