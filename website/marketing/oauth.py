"""Get a valid Google access token using the stored marketing refresh token."""
import json
import urllib.request
import urllib.parse
import os

TOKEN_URL = 'https://oauth2.googleapis.com/token'


def get_access_token():
    refresh_token = os.environ.get('GOOGLE_MARKETING_REFRESH_TOKEN', '')
    client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID', '')
    client_secret = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET', '')

    if not all([refresh_token, client_id, client_secret]):
        return None

    body = urllib.parse.urlencode({
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
    }).encode()

    try:
        req = urllib.request.Request(TOKEN_URL, data=body, method='POST')
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        return data.get('access_token')
    except Exception as e:
        print(f'[marketing.oauth] Token refresh failed: {e}')
        return None
