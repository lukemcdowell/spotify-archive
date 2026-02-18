import os
import sys
import base64
import json
import time
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import threading
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = 'http://127.0.0.1:8888/callback'

if not CLIENT_ID or not CLIENT_SECRET:
    print('Set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET as environment variables.')
    sys.exit(1)

SCOPE = 'user-top-read playlist-modify-private'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH = os.path.join(SCRIPT_DIR, '..', 'cdk', 'lambda', '.cache')


def get_tokens(code):
    credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(
        'https://accounts.spotify.com/api/token',
        headers=headers,
        data=data
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Token request failed: {response.text}")


class CallbackHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        if 'code' in query_params:
            code = query_params['code'][0]

            try:
                tokens = get_tokens(code)

                cache = {
                    "access_token": tokens["access_token"],
                    "token_type": tokens["token_type"],
                    "expires_in": tokens["expires_in"],
                    "refresh_token": tokens["refresh_token"],
                    "scope": tokens["scope"],
                    "expires_at": int(time.time()) + tokens["expires_in"],
                }
                with open(CACHE_PATH, 'w') as f:
                    json.dump(cache, f)
                print(f'\nCache file written to: {os.path.abspath(CACHE_PATH)}')

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                html = f"""
                <html>
                    <body>
                        <h1>Success!</h1>
                        <p>Your refresh token:</p>
                        <pre style="background: #f0f0f0; padding: 10px;">{tokens['refresh_token']}</pre>
                        <p>Access token (expires in 1 hour):</p>
                        <pre style="background: #f0f0f0; padding: 10px;">{tokens['access_token']}</pre>
                    </body>
                </html>
                """

                self.wfile.write(html.encode())

                # Shutdown server after a short delay
                threading.Timer(1.0, lambda: self.server.shutdown()).start()

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>".encode())

    def log_message(self, format, *args):
        pass


def main():
    server = HTTPServer(('localhost', 8888), CallbackHandler)

    auth_url = (
        f"https://accounts.spotify.com/authorize?"
        f"response_type=code&"
        f"client_id={CLIENT_ID}&"
        f"scope={urllib.parse.quote(SCOPE)}&"
        f"redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
    )

    print('Click this URL to authorize:\n')
    print(auth_url)
    print('\nWaiting for authorization...\n')

    server.serve_forever()
    print('\nAuthorization complete!')


if __name__ == '__main__':
    main()
