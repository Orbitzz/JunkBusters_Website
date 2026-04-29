"""Send messages to the Junk Busters Marketing Telegram channel."""
import json
import os
import urllib.request


def send(message, parse_mode='HTML'):
    token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    channel_id = os.environ.get('TELEGRAM_CHANNEL_ID', '')

    if not token or not channel_id:
        print('[telegram] TELEGRAM_BOT_TOKEN or TELEGRAM_CHANNEL_ID not set')
        return False

    url = f'https://api.telegram.org/bot{token}/sendMessage'

    # Split at newline boundaries if message exceeds Telegram's 4096 char limit
    chunks = []
    while len(message) > 4096:
        split_at = message.rfind('\n', 0, 4096)
        if split_at == -1:
            split_at = 4096
        chunks.append(message[:split_at])
        message = message[split_at:].lstrip('\n')
    chunks.append(message)

    success = True
    for chunk in chunks:
        body = json.dumps({
            'chat_id': channel_id,
            'text': chunk,
            'parse_mode': parse_mode,
        }).encode()
        req = urllib.request.Request(url, data=body, method='POST')
        req.add_header('Content-Type', 'application/json')
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read())
                if not result.get('ok'):
                    print(f'[telegram] Send failed: {result}')
                    success = False
        except Exception as e:
            print(f'[telegram] Exception: {e}')
            success = False

    return success
