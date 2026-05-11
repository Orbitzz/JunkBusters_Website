"""
One-time OAuth flow for marketing agent (GSC + GA4 read access).
Visit /marketing-auth/start/ to authorize. The callback displays the refresh token
to copy into Railway as GOOGLE_MARKETING_REFRESH_TOKEN.
"""
import json
import urllib.request
import urllib.parse
import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect

SCOPES = ' '.join([
    'https://www.googleapis.com/auth/webmasters.readonly',
    'https://www.googleapis.com/auth/analytics.readonly',
])
AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'


def marketing_auth_start(request):
    client_id = getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', '')
    redirect_uri = getattr(settings, 'GOOGLE_MARKETING_REDIRECT_URI', '')
    if not client_id:
        return HttpResponse('GOOGLE_OAUTH_CLIENT_ID not configured.', status=500)
    params = urllib.parse.urlencode({
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': SCOPES,
        'access_type': 'offline',
        'prompt': 'consent',
    })
    return redirect(f'{AUTH_URL}?{params}')


def marketing_auth_callback(request):
    error = request.GET.get('error')
    if error:
        return HttpResponse(f'<h2>OAuth Error: {error}</h2>', status=400)

    code = request.GET.get('code')
    if not code:
        return HttpResponse('<h2>No authorization code received.</h2>', status=400)

    client_id = getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', '')
    client_secret = getattr(settings, 'GOOGLE_OAUTH_CLIENT_SECRET', '')
    redirect_uri = getattr(settings, 'GOOGLE_MARKETING_REDIRECT_URI', '')

    body = urllib.parse.urlencode({
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }).encode()

    try:
        req = urllib.request.Request(TOKEN_URL, data=body, method='POST')
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        return HttpResponse(f'<h2>Token exchange failed: {e}</h2>', status=500)

    if 'error' in data:
        return HttpResponse(
            f'<h2>Token error: {data["error"]} — {data.get("error_description", "")}</h2>',
            status=400,
        )

    refresh_token = data.get('refresh_token', '')
    if not refresh_token:
        return HttpResponse(
            '<html><body style="font-family:sans-serif;max-width:600px;margin:60px auto;">'
            '<h2 style="color:#dc2626;">No refresh token returned.</h2>'
            '<p>Google only issues a refresh token on the first authorization. '
            'Go to <a href="https://myaccount.google.com/permissions">myaccount.google.com/permissions</a>, '
            'revoke access for this app, then visit '
            '<a href="/marketing-auth/start/">/marketing-auth/start/</a> again.</p>'
            '</body></html>',
            status=400,
        )

    return HttpResponse(f"""
    <html><body style="font-family:sans-serif;max-width:700px;margin:60px auto;padding:0 24px;">
    <h2 style="color:#1a2e4a;">Marketing Agent Authorized</h2>
    <p>Copy the refresh token below and add it as <code>GOOGLE_MARKETING_REFRESH_TOKEN</code>
    in your Railway project variables.</p>
    <div style="background:#f0f4f8;border:2px solid #1a2e4a;border-radius:8px;padding:20px 24px;margin:20px 0;">
      <p style="font-size:11px;color:#64748b;margin:0 0 8px;font-weight:600;letter-spacing:.05em;">
        GOOGLE_MARKETING_REFRESH_TOKEN</p>
      <code style="font-size:13px;word-break:break-all;color:#1a2e4a;display:block;">{refresh_token}</code>
    </div>
    <ol style="color:#374151;line-height:2;">
      <li>Copy the token above</li>
      <li>Go to Railway → your project → Variables tab</li>
      <li>Add variable: <code>GOOGLE_MARKETING_REFRESH_TOKEN</code></li>
      <li>Paste the token as the value and save</li>
    </ol>
    <p style="color:#64748b;font-size:14px;">Once saved, the weekly cron job will use this token automatically.</p>
    </body></html>
    """)


def marketing_run_report(request):
    """One-time manual trigger: /marketing-auth/run-report/?token=jb2026"""
    if request.GET.get('token') != 'jb2026':
        return HttpResponse('Forbidden', status=403)
    import io, sys
    from website.marketing import oauth, gsc, ga4, auditor, report, telegram, sitemap_checker, pagespeed, omnihq_sync
    buf = io.StringIO()

    def log(msg):
        buf.write(msg + '\n')

    log('Getting Google access token...')
    token = oauth.get_access_token()

    if token:
        log('Fetching GSC data...')
        gsc_data = gsc.fetch_report(token)
        log(f'GSC result: {"error: " + gsc_data["error"] if gsc_data and "error" in gsc_data else "ok"}')
        log('Fetching GA4 data...')
        ga4_data = ga4.fetch_report(token)
        log(f'GA4 result: {"error: " + ga4_data["error"] if ga4_data and "error" in ga4_data else "ok"}')
    else:
        log('No Google token — audit only')
        gsc_data = None
        ga4_data = None

    log('Auditing site pages...')
    audit_data = auditor.audit_pages()
    log(f'Audited {len(audit_data)} pages')

    log('Checking sitemap health...')
    sitemap_data = sitemap_checker.check_sitemap()
    nf = len(sitemap_data.get('not_found', [])) if 'error' not in sitemap_data else '?'
    log(f'Sitemap: {sitemap_data.get("total", "?")} URLs, {nf} 404s')

    log('Checking page speed...')
    speed_data = pagespeed.check_speed()
    log(f'Speed checked {len(speed_data)} pages')

    log('Building report...')
    message = report.build(gsc_data, ga4_data, audit_data, sitemap_data, speed_data)

    log('Sending to Telegram...')
    ok = telegram.send(message)
    log(f'Telegram send: {"SUCCESS" if ok else "FAILED"}')

    log('Syncing to OmniHQ...')
    synced = omnihq_sync.post_report(gsc_data, ga4_data, audit_data, sitemap_data, speed_data)
    log(f'OmniHQ sync: {"ok" if synced else "skipped/failed (non-critical)"}')

    log('')
    log('--- Report preview ---')
    log(message)

    return HttpResponse(buf.getvalue().replace('\n', '<br>'), content_type='text/html')


def marketing_telegram_id(request):
    """Display Telegram channel IDs seen by the bot. Forward a channel message to the bot first."""
    token = os.environ.get('TELEGRAM_BOT_TOKEN', getattr(settings, 'TELEGRAM_BOT_TOKEN', ''))
    if not token:
        return HttpResponse('TELEGRAM_BOT_TOKEN not configured.', status=500)

    try:
        url = f'https://api.telegram.org/bot{token}/getUpdates?limit=100'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        return HttpResponse(f'<h2>Telegram API error: {e}</h2>', status=500)

    chats = {}
    for update in data.get('result', []):
        for key in ('message', 'channel_post', 'edited_message', 'edited_channel_post'):
            msg = update.get(key) or {}
            chat = msg.get('chat', {})
            if chat.get('id'):
                chats[chat['id']] = {
                    'id': chat['id'],
                    'title': chat.get('title') or chat.get('first_name', 'Unknown'),
                    'type': chat.get('type', ''),
                }
            fwd = msg.get('forward_from_chat', {})
            if fwd.get('id'):
                chats[fwd['id']] = {
                    'id': fwd['id'],
                    'title': fwd.get('title', 'Unknown'),
                    'type': fwd.get('type', ''),
                }

    channels = {k: v for k, v in chats.items() if v['type'] in ('channel', 'supergroup', 'group')}

    if not channels:
        body = """
        <p style="color:#dc2626;font-weight:bold;">No channels found yet.</p>
        <ol style="line-height:2.2;">
          <li>Open your <strong>Junk Busters Marketing</strong> channel in Telegram</li>
          <li>Add <strong>@JBMarketingbot</strong> as an Admin</li>
          <li>In Telegram, open a direct chat with <strong>@JBMarketingbot</strong></li>
          <li>Forward any message from the <strong>Junk Busters Marketing</strong> channel to the bot</li>
          <li>Refresh this page</li>
        </ol>
        """
    else:
        rows = ''.join(
            f'<tr style="border-bottom:1px solid #e2e8f0;">'
            f'<td style="padding:10px 14px;font-weight:600;">{v["title"]}</td>'
            f'<td style="padding:10px 14px;font-family:monospace;font-size:15px;">{v["id"]}</td>'
            f'<td style="padding:10px 14px;color:#64748b;">{v["type"]}</td></tr>'
            for v in channels.values()
        )
        body = f"""
        <p>Add the channel ID as <code>TELEGRAM_CHANNEL_ID</code> in Railway variables:</p>
        <table style="border-collapse:collapse;width:100%;margin:16px 0;">
          <thead><tr style="background:#1a2e4a;color:#fff;">
            <th style="padding:10px 14px;text-align:left;">Channel</th>
            <th style="padding:10px 14px;text-align:left;">ID (copy this)</th>
            <th style="padding:10px 14px;text-align:left;">Type</th>
          </tr></thead>
          <tbody>{rows}</tbody>
        </table>
        """

    return HttpResponse(f"""
    <html><body style="font-family:sans-serif;max-width:700px;margin:60px auto;padding:0 24px;">
    <h2 style="color:#1a2e4a;">Telegram Channel ID Lookup</h2>
    {body}
    </body></html>
    """)
