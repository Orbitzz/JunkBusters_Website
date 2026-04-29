"""Assemble the weekly Telegram marketing report (HTML parse mode)."""
from datetime import date


def _e(text):
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _delta(pct):
    if pct > 0:
        return f'+{pct}%'
    return f'{pct}%'


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
                page = _e(d['page'].replace('https://junkbusterstn.com', ''))
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
                lines.append(f'  • {_e(p["page"])} — {p["key_events"]} key events')

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

        if red:
            top = red[0]['slug']
            lines.append('<b>Priority This Week</b>')
            lines.append(f'Expand {top} — thin content + high commercial intent = highest ROI')

    return '\n'.join(lines)
