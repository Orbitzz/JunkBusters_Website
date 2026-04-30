"""Assemble the weekly Telegram marketing report (HTML parse mode)."""
from datetime import date


def _e(text):
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _delta(pct):
    arrow = '+' if pct > 0 else ''
    return f'{arrow}{pct}%'


def _strip_domain(url):
    for prefix in ('https://www.junkbustershauling.com', 'https://junkbustershauling.com'):
        if url.startswith(prefix):
            path = url[len(prefix):]
            return path or '/'
    return url


def _duration(seconds):
    m, s = divmod(int(seconds), 60)
    return f'{m}m {s}s' if m else f'{s}s'


def _speed_icon(score):
    if score >= 90:
        return '✅'
    if score >= 50:
        return '🟡'
    return '🔴'


# ── Priority action builder ───────────────────────────────────────────────────

def _build_actions(gsc_data, ga4_data, audit_data, sitemap_data, speed_data):
    actions = []
    red_pages = [p for p in (audit_data or []) if p.get('priority') == 'red' and 'error' not in p]

    # 1. Broken page in sitemap → fix immediately
    if sitemap_data and 'error' not in sitemap_data:
        for url in (sitemap_data.get('not_found') or [])[:2]:
            path = _strip_domain(url)
            actions.append(f'Fix 404 in sitemap: {_e(path)} — Google is crawling a broken URL. Add a redirect or restore the page.')

    # 2. Page-2 keyword aligned with a thin/red audit page = highest content ROI
    if gsc_data and 'error' not in gsc_data:
        for page in red_pages:
            slug_words = set(page['slug'].strip('/').replace('-', ' ').split())
            for p2 in gsc_data.get('page2', []):
                query = p2['keys'][0].lower()
                if slug_words & set(query.split()):
                    impr = p2['impressions']
                    pos = round(p2['position'], 1)
                    actions.append(
                        f'Expand {_e(page["slug"])} — page-2 keyword "{_e(query)}" '
                        f'({impr} impr · pos {pos}) + thin content. '
                        f'Add 300+ words + FAQs to push onto page 1.'
                    )
                    break

    # 3. High impressions + very low CTR → title/meta description is wrong
    if gsc_data and 'error' not in gsc_data:
        for r in (gsc_data.get('ctr_opps') or [])[:1]:
            q = _e(r['keys'][0])
            ctr = round(r.get('ctr', 0) * 100, 1)
            actions.append(
                f'Fix title tag for "{q}" — {r["impressions"]} impressions, only {ctr}% CTR. '
                f'Rewrite the page title and meta description to be more specific and click-worthy.'
            )

    # 4. Traffic with zero conversions → CTA gap
    if ga4_data and 'error' not in ga4_data:
        for p in (ga4_data.get('needs_cta') or [])[:1]:
            actions.append(
                f'Add quote CTA to {_e(p["page"])} — {p["sessions"]} sessions, 0 conversions. '
                f'Place a visible "Get a Free Estimate" button above the fold.'
            )

    # 5. Poor page speed → ranking penalty
    if speed_data:
        for p in speed_data:
            if 'error' not in p and p.get('score', 100) < 50:
                actions.append(
                    f'Fix page speed on {_e(p["slug"])} — score {p["score"]}/100 (Poor). '
                    f'LCP: {p.get("lcp", "N/A")}. Compress images and defer non-critical JS.'
                )

    # 6. Declining pages → content refresh
    if gsc_data and 'error' not in gsc_data:
        for d in (gsc_data.get('declining') or [])[:1]:
            path = _e(_strip_domain(d['page']))
            actions.append(
                f'Refresh {path} — clicks dropped {d["pct"]}% ({d["prev"]} → {d["clicks"]}). '
                f'Update copy, add internal links, and resubmit to GSC.'
            )

    # 7. Zero-click keyword = content gap (no page targeting it)
    if gsc_data and 'error' not in gsc_data:
        for r in (gsc_data.get('zero_click') or [])[:1]:
            q = _e(r['keys'][0])
            actions.append(
                f'Create content for "{q}" — {r["impressions"]} impressions, 0 clicks. '
                f'No page is targeting this keyword. Add a section or new page.'
            )

    # 8. Remaining red audit pages (fallback)
    covered = set()
    for a in actions:
        for p in red_pages:
            if p['slug'] in a:
                covered.add(p['slug'])
    for page in red_pages:
        if page['slug'] not in covered and len(actions) < 4:
            actions.append(
                f'Expand {_e(page["slug"])} — {page["words"]} words, {page["faqs"]} FAQs, no schema. '
                f'Add content + FAQ section.'
            )

    return actions[:4]


# ── Report builder ────────────────────────────────────────────────────────────

def build(gsc_data, ga4_data, audit_data, sitemap_data=None, speed_data=None):
    lines = []
    week = date.today().strftime('%B %d, %Y')
    lines += [f'<b>JB Marketing Report — {week}</b>', '']

    # ── Search Console ────────────────────────────────────────────────────────
    if gsc_data is None:
        lines += ['<i>GSC: not configured — run /marketing-auth/start/</i>', '']
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
        nb = g.get('non_brand_clicks', 0)
        tot = g.get('total_clicks', 0)
        bp = g.get('brand_pct', 0)
        lines.append(
            f'Non-brand clicks: {nb} of {tot} ({100 - bp}%) — '
            f'brand: {g.get("brand_clicks", 0)} ({bp}%)'
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
            lines.append('<b>Page 2 Opportunities</b>')
            for r in g['page2']:
                q = _e(r['keys'][0])
                lines.append(f'• "{q}" — {r["impressions"]} impr · pos {round(r["position"], 1)}')
            lines.append('')

        if g.get('ctr_opps'):
            lines.append('<b>Low CTR — Fix Title Tags</b>')
            for r in g['ctr_opps']:
                q = _e(r['keys'][0])
                ctr = round(r.get('ctr', 0) * 100, 1)
                lines.append(f'• "{q}" — {r["impressions"]} impr · {ctr}% CTR')
            lines.append('')

        if g.get('zero_click'):
            lines.append('<b>Zero-Click Keywords (Content Gaps)</b>')
            for r in g['zero_click']:
                q = _e(r['keys'][0])
                lines.append(f'• "{q}" — {r["impressions"]} impr · 0 clicks')
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
        lines.append(
            f'Sessions: {a["total_sessions"]:,} ({_delta(a["session_delta"])})  '
            f'New users: {a.get("new_users", "—"):,}'
        )
        lines.append(
            f'Engagement: {a.get("engagement_rate", "—")}%  '
            f'Avg duration: {_duration(a.get("avg_duration", 0))}  '
            f'Page views: {a.get("page_views", "—"):,}'
        )

        if a.get('top_converters'):
            lines.append('Top converters:')
            for p in a['top_converters']:
                lines.append(f'  • {_e(p["page"])} — {p["conversions"]} conversions')

        if a.get('needs_cta'):
            lines.append('Needs CTA work:')
            for p in a['needs_cta']:
                lines.append(f'  • {_e(p["page"])} — {p["sessions"]} sessions, 0 conversions')

        lines.append('')

    # ── Site Health (sitemap checker) ─────────────────────────────────────────
    if sitemap_data:
        lines.append('<b>Site Health</b>')
        if 'error' in sitemap_data:
            lines.append(f'<i>Sitemap check failed: {_e(sitemap_data["error"])}</i>')
        else:
            total = sitemap_data['total']
            ok = sitemap_data['ok']
            nf = sitemap_data.get('not_found', [])
            redir = sitemap_data.get('redirects', [])
            errs = sitemap_data.get('errors', [])
            lines.append(f'Sitemap: {total} URLs checked — ✅ {ok} ok  ⚠️ {len(redir)} redirect  ❌ {len(nf)} 404')
            for url in nf[:5]:
                lines.append(f'  ❌ {_e(_strip_domain(url))}')
            for url in redir[:3]:
                lines.append(f'  ⚠️ {_e(_strip_domain(url))} (redirecting)')
            if errs:
                lines.append(f'  {len(errs)} other errors')
        lines.append('')

    # ── Page Speed ────────────────────────────────────────────────────────────
    if speed_data:
        lines.append('<b>Page Speed (Mobile)</b>')
        for p in speed_data:
            if 'error' in p:
                lines.append(f'  {_e(p["slug"])} — check failed')
            else:
                icon = _speed_icon(p['score'])
                lines.append(
                    f'  {icon} {_e(p["slug"])} — {p["score"]}/100  '
                    f'LCP: {p.get("lcp", "N/A")}  CLS: {p.get("cls", "N/A")}'
                )
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
                schema = 'schema ✓' if p['has_schema'] else 'no schema'
                lines.append(f'🔴 {p["slug"]} — {p["words"]} words, {p["faqs"]} FAQs, {schema}')

        for p in yellow:
            schema = 'schema ✓' if p['has_schema'] else 'no schema'
            lines.append(f'🟡 {p["slug"]} — {p["words"]} words, {p["faqs"]} FAQs, {schema}')

        for p in green:
            lines.append(f'✅ {p["slug"]} — {p["words"]} words, {p["faqs"]} FAQs ✓')

        lines.append('')

    # ── Priority Actions ──────────────────────────────────────────────────────
    actions = _build_actions(gsc_data, ga4_data, audit_data, sitemap_data, speed_data)
    if actions:
        lines.append('<b>Priority Actions This Week</b>')
        for i, action in enumerate(actions, 1):
            lines.append(f'{i}. {action}')

    return '\n'.join(lines)
