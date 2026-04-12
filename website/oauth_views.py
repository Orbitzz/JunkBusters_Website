"""
Google OAuth2 views for Business Profile API authorization.
Visit /google-auth/start/ to begin the OAuth flow.
This only needs to be done once — the refresh token is stored locally.
"""
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect

TOKEN_FILE = Path(__file__).parent / '_oauth_tokens.json'

SCOPES = 'https://www.googleapis.com/auth/business.manage'
AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'


def google_auth_start(request):
    client_id = getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', '')
    redirect_uri = getattr(settings, 'GOOGLE_OAUTH_REDIRECT_URI', '')
    if not client_id:
        return HttpResponse('GOOGLE_OAUTH_CLIENT_ID not configured in settings.', status=500)

    params = urllib.parse.urlencode({
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': SCOPES,
        'access_type': 'offline',
        'prompt': 'consent',
    })
    return redirect(f'{AUTH_URL}?{params}')


def google_auth_callback(request):
    error = request.GET.get('error')
    if error:
        return HttpResponse(f'<h2>OAuth Error: {error}</h2>', status=400)

    code = request.GET.get('code')
    if not code:
        return HttpResponse('<h2>No authorization code received.</h2>', status=400)

    client_id = getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', '')
    client_secret = getattr(settings, 'GOOGLE_OAUTH_CLIENT_SECRET', '')
    redirect_uri = getattr(settings, 'GOOGLE_OAUTH_REDIRECT_URI', '')

    # Exchange code for tokens
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
        return HttpResponse(f'<h2>Token error: {data["error"]} — {data.get("error_description", "")}</h2>', status=400)

    tokens = {
        'access_token': data.get('access_token'),
        'refresh_token': data.get('refresh_token'),
        'expires_at': time.time() + data.get('expires_in', 3600) - 60,
    }
    TOKEN_FILE.write_text(json.dumps(tokens))

    # Delete cache so next page load fetches fresh reviews
    cache_file = Path(__file__).parent / '_google_reviews_cache.json'
    if cache_file.exists():
        cache_file.unlink()

    return HttpResponse("""
    <html><body style="font-family:sans-serif;max-width:600px;margin:60px auto;text-align:center;">
    <h2 style="color:#1a2e4a;">&#10003; Google Business Profile connected!</h2>
    <p>Refresh token saved. Your website will now fetch all reviews from Google Business Profile.</p>
    <p>The review cache has been cleared — the next page load will pull live reviews.</p>
    <a href="/" style="background:#f5c800;color:#1a2e4a;padding:12px 24px;border-radius:6px;
       text-decoration:none;font-weight:700;display:inline-block;margin-top:16px;">
       Go to Homepage</a>
    </body></html>
    """)


def google_auth_clear_cache(request):
    """Clear the reviews cache so the next page load fetches fresh data."""
    cache_file = Path(__file__).parent / '_google_reviews_cache.json'
    if cache_file.exists():
        cache_file.unlink()
        msg = 'Cache cleared. Next page load will fetch fresh reviews.'
    else:
        msg = 'No cache file found.'
    return HttpResponse(f"""
    <html><body style="font-family:sans-serif;max-width:600px;margin:60px auto;text-align:center;">
    <h2>{msg}</h2>
    <a href="/" style="background:#1a2e4a;color:#fff;padding:10px 20px;border-radius:6px;
       text-decoration:none;font-weight:700;">Go to Homepage</a>
    </body></html>
    """)


def google_auth_status(request):
    """Show current auth status and token info."""
    if TOKEN_FILE.exists():
        try:
            tokens = json.loads(TOKEN_FILE.read_text())
            has_refresh = bool(tokens.get('refresh_token'))
            expires_at = tokens.get('expires_at', 0)
            expired = time.time() > expires_at
            status_html = f"""
            <p><strong>Status:</strong> &#10003; Tokens stored</p>
            <p><strong>Refresh token:</strong> {'Present' if has_refresh else 'Missing'}</p>
            <p><strong>Access token:</strong> {'Expired (will auto-refresh)' if expired else 'Valid'}</p>
            """
        except Exception:
            status_html = '<p>Token file exists but could not be read.</p>'
    else:
        status_html = '<p><strong>Status:</strong> Not connected — no tokens stored.</p>'

    return HttpResponse(f"""
    <html><body style="font-family:sans-serif;max-width:600px;margin:60px auto;">
    <h2 style="color:#1a2e4a;">Google Business Profile — Auth Status</h2>
    {status_html}
    <br>
    <a href="/google-auth/start/" style="background:#1a2e4a;color:#fff;padding:10px 20px;
       border-radius:6px;text-decoration:none;font-weight:700;">Re-authorize</a>
    &nbsp;
    <a href="/google-auth/clear-cache/" style="background:#f5c800;color:#1a2e4a;padding:10px 20px;
       border-radius:6px;text-decoration:none;font-weight:700;">Clear Review Cache</a>
    &nbsp;
    <a href="/" style="color:#1a2e4a;">← Home</a>
    </body></html>
    """)
