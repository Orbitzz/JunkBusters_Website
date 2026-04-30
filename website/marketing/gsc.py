"""Google Search Console API client — search analytics with full CMO-level signals."""
import json
import os
import urllib.request
import urllib.parse
from datetime import date, timedelta

BRAND_TERMS = ('junk busters', 'junkbusters', 'junk buster')


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
        curr_rows = query(start, end, ['query'], 50)
        prior_rows = query(prior_start, prior_end, ['query'], 50)
        curr_pages = query(start, end, ['page'], 25)
        prior_pages = query(prior_start, prior_end, ['page'], 25)

        prior_query_clicks = {r['keys'][0]: r['clicks'] for r in prior_rows}
        prior_page_clicks = {r['keys'][0]: r['clicks'] for r in prior_pages}

        # ── Core metrics ──────────────────────────────────────────────────────
        total_clicks = sum(r['clicks'] for r in curr_rows)
        total_impressions = sum(r['impressions'] for r in curr_rows)
        prior_total = sum(r['clicks'] for r in prior_rows)
        click_delta = round((total_clicks - prior_total) / prior_total * 100) if prior_total else 0

        weighted_pos = sum(r['position'] * r['impressions'] for r in curr_rows)
        total_impr = sum(r['impressions'] for r in curr_rows)
        avg_position = round(weighted_pos / total_impr, 1) if total_impr else 0

        # ── Brand vs non-brand ────────────────────────────────────────────────
        brand_clicks = sum(
            r['clicks'] for r in curr_rows
            if any(t in r['keys'][0].lower() for t in BRAND_TERMS)
        )
        non_brand_clicks = total_clicks - brand_clicks
        brand_pct = round(brand_clicks / total_clicks * 100) if total_clicks else 0

        # ── Top queries by clicks ─────────────────────────────────────────────
        top_queries = sorted(curr_rows, key=lambda r: r['clicks'], reverse=True)[:10]

        # ── Page 2 opportunities (pos 11-20, sorted by impressions) ──────────
        page2 = sorted(
            [r for r in curr_rows if 11 <= r.get('position', 0) <= 20],
            key=lambda r: r['impressions'],
            reverse=True,
        )[:5]

        # ── CTR opportunities: high impressions, low CTR (<2%) ───────────────
        ctr_opps = sorted(
            [r for r in curr_rows if r['impressions'] >= 100 and r.get('ctr', 1) < 0.02],
            key=lambda r: r['impressions'],
            reverse=True,
        )[:5]

        # ── Zero-click keywords: impressions but never clicked ────────────────
        zero_click = sorted(
            [r for r in curr_rows if r['clicks'] == 0 and r['impressions'] >= 50],
            key=lambda r: r['impressions'],
            reverse=True,
        )[:5]

        # ── Declining pages (>20% week-over-week click drop) ─────────────────
        declining = []
        for r in curr_pages:
            page = r['keys'][0]
            prev = prior_page_clicks.get(page, 0)
            curr_c = r['clicks']
            if prev > 2 and curr_c < prev * 0.8:
                pct = round((curr_c - prev) / prev * 100)
                declining.append({'page': page, 'clicks': curr_c, 'prev': prev, 'pct': pct})
        declining = sorted(declining, key=lambda x: x['pct'])[:3]

        return {
            'total_clicks': total_clicks,
            'total_impressions': total_impressions,
            'avg_position': avg_position,
            'click_delta': click_delta,
            'brand_clicks': brand_clicks,
            'non_brand_clicks': non_brand_clicks,
            'brand_pct': brand_pct,
            'top_queries': top_queries,
            'page2': page2,
            'ctr_opps': ctr_opps,
            'zero_click': zero_click,
            'declining': declining,
            'date_range': f'{start.isoformat()} → {end.isoformat()}',
        }
    except Exception as e:
        return {'error': str(e)}
