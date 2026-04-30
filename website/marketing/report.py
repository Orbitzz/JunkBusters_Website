"""Assemble the weekly Telegram marketing report (HTML parse mode)."""
from datetime import date


def _e(text):
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _delta(pct):
    if pct > 0:
        return f'+{pct}%'
    return f'{pct}%'


def _strip_domain(url):
    for prefix in ('https://www.junkbustershauling.com', 'https://junkbustershauling.com'):
        if url.startswith(prefix):
            return url[len(prefix):]
    return url


def _build_actions(gsc_data, ga4_data, audit_data):
    """Return up to 3 specific, data-driven action items for the week."""
    actions = []
    red_pages = [p for p in (audit_data or []) if p.get('priority') == 'red' and 'error' not in p]

    # Signal 1: page-2 keyword whose words overlap a thin/red audit page = best ROI
    if gsc_data and 'error' not in gsc_data:
        for page in red_pages:
            slug_words = set(page['slug'].strip('/').replace('-', ' ').split())
            for p2 in gsc_data.get('page2', []):
                query = p2['keys'][0].lower()
                if slug_words & set(query.split()):
                    impr = p2['impressions']
                    pos = round(p2['position'], 1)
                    actions.append(
                        f'Expand {page["slug"]} — page-2 keyword "{_e(query)}" '
                        f'({impr} impr · pos {pos}) aligns with thin page. '
                        f'Add 300+ words + FAQs to push to page 1.'
                    )
                    break

    # Signal 2: pages with traffic but zero conversions → CTA gap
    if ga4_data and 'error' not in ga4_data:
        for p in ga4_data.get('needs_cta', [])[:2]:
            actions.append(
                f'Add a quote CTA to {_e(p["page"])} — '
                f'{p["sessions"]} sessions this week, 0 conversions. '
                f'A visible "Get a Free Estimate" button above the fold could recover leads.'
            )

    # Signal 3: declining pages → content refresh
    if gsc_data and 'error' not in gsc_data:
        for d in gsc_data.get('declining', [])[:1]:
            path = _e(_strip_domain(d['page']))
            actions.append(
                f'Refresh {path} — clicks dropped {d["pct"]}% week-over-week '
                f'({d["prev"]} → {d["clicks"]}). Update the page copy and internal links.'
            )

    # Signal 4: red audit pages not already covered (fallback)
    covered_slugs = set()
    for a in actions:
        for page in red_pages:
            if page['slug'] in a:
                covered_slugs.add(page['slug'])
    for page in red_pages:
        if page['slug'] not in covered_slugs and len(actions) < 3:
            actions.append(
                f'Expand {page["slug"]} — {page["words"]} words, {page["faqs"]} FAQs, '
                f'no schema. Add content + FAQ section to reach green status.'
            )

    return actions[:3]


def build(gsc_data, ga4_data, audit_data):
    lines = []
    week = date.today().strftime('%B %d, %Y')
    lines += [f'<b>JB Marketing Report — {week}</b>', '']

    # ── Search Console ────────────────────────────────────────────────────────
    if gsc_data is None:
        lines += ['<i>GSC: GOOGLE_MARKETING_REFRESH_TOKEN not set — run /marketing-auth/start/</i>', '']
    elif 'error' in gsc_data:
        lines += [f'<i>GSC error: {_e(gsc_data["error"])}</i>', '']
    else:
        g = gsc_data
        lines.append('<b>Search Console (Last 7 Days)</b>')
        lines.append(
            f'Clicks: {g["total_clicks"]:,} ({_delta(g["click_delta"])})  '
            f'Impressions: {g["total_impressions"]:,}  '
            f'Avg pos: {g["avg_position"]}'
        )
        lines.append(f'<i>{g["date_range"]}</i>')
        lines.append('')

        if g.get('top_queries'):
            lines.append('<b>Top Queries by Clicks</b>')
            for i, r in enumerate(g['top_queries'][:8], 1):
                q = _e(r['keys'][0])
                lines.append(f'{i}. {q} — {r["clicks"]} clicks · pos {round(r["position"], 1)}')
            lines.append('')

        if g.get('page2'):
            lines.append('<b>Page 2 Opportunities — Act on These</b>')
            for r in g['page2']:
                q = _e(r['keys'][0])
                lines.append(f'• "{q}" — {r["impressions"]} impr · pos {round(r["position"], 1)}')
            lines.append('')

        if g.get('declining'):
            lines.append('<b>Declining Pages</b>')
            for d in g['declining']:
                page = _e(_strip_domain(d['page']))
                lines.append(f'• {page} — {d["clicks"]} clicks ({_delta(d["pct"])} vs prior week)')
            lines.append('')

    # ── GA4 ──────────────────────────────────────────────────────────────────
    if ga4_data is None:
        pass
    elif 'error' in ga4_data:
        lines += [f'<i>GA4 error: {_e(ga4_data["error"])}</i>', '']
    else:
        a = ga4_data
        lines.append('<b>GA4 (Last 7 Days)</b>')
        lines.append(f'Sessions: {a["total_sessions"]:,} ({_delta(a["session_delta"])})')

        if a.get('top_converters'):
            lines.append('Top converters:')
            for p in a['top_converters']:
                lines.append(f'  • {_e(p["page"])} — {p["conversions"]} conversions')

        if a.get('needs_cta'):
            lines.append('Needs CTA work:')
            for p in a['needs_cta']:
                lines.append(f'  • {_e(p["page"])} — {p["sessions"]} sessions, 0 conversions')

        lines.append('')

    # ── Content Audit ─────────────────────────────────────────────────────────
    if audit_data:
        lines.append('<b>Content Audit</b>')
        red = [p for p in audit_data if p.get('priority') == 'red']
        yellow = [p for p in audit_data if p.get('priority') == 'yellow']
        green = [p for p in audit_data if p.get('priority') == 'green']

        for p in red:
            if 'error' in p:
                lines.append(f'🔴 {p["slug"]} — fetch error')
            else:
                schema = 'schema' if p['has_schema'] else 'no schema'
                lines.append(f'🔴 {p["slug"]} — {p["words"]} words, {p["faqs"]} FAQs, {schema}')

        for p in yellow:
            schema = 'schema ✓' if p['has_schema'] else 'no schema'
            lines.append(f'🟡 {p["slug"]} — {p["words"]} words, {p["faqs"]} FAQs, {schema}')

        for p in green:
            lines.append(f'✅ {p["slug"]} — {p["words"]} words, {p["faqs"]} FAQs ✓')

        lines.append('')

    # ── Data-driven actions ───────────────────────────────────────────────────
    actions = _build_actions(gsc_data, ga4_data, audit_data)
    if actions:
        lines.append('<b>Priority Actions This Week</b>')
        for i, action in enumerate(actions, 1):
            lines.append(f'{i}. {action}')

    return '\n'.join(lines)
