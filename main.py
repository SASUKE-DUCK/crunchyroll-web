import uuid 
from http.cookiejar import MozillaCookieJar
import json
import requests
from tls_client import Session
from datetime import datetime
from urllib.parse import urlencode
from endpoints import (
    CRUNCHYROLL_AUTH_ENDPOINT,
    CRUNCHYROLL_CONTENT_ENDPOINT,
    CRUNCHYROLL_PLAY_ENDPOINT,
    DRM_AUTH_ENDPOINT,
)

video_id = 'GJWU2M0QX'

session = Session(client_identifier="chrome112", random_tls_extension_order=True)

cookie_file = "cookies.txt"
cookie_jar = MozillaCookieJar()

try:
    cookie_jar.load(cookie_file, ignore_discard=True, ignore_expires=True)
    session.cookies = cookie_jar
except FileNotFoundError:
    print(f"Cookies file '{cookie_file}' not found.")

cookie_dict = {cookie.name: cookie.value for cookie in session.cookies}
session_id = cookie_dict.get('session_id', '')

device_id = str(uuid.uuid4())

headers_auth = {
    'authorization': 'Basic bm9haWhkZXZtXzZpeWcwYThsMHE6',
    'etp-anonymous-id': device_id,
    'origin': 'https://www.crunchyroll.com',
    'referer': 'https://www.crunchyroll.com/pt-br',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0',
}

data_auth = {
    'device_id': device_id,
    'device_type': 'Opera on Windows',
    'grant_type': 'etp_rt_cookie',
}

response_token_license = session.post(CRUNCHYROLL_AUTH_ENDPOINT, headers=headers_auth, data=data_auth)
response_json = json.loads(response_token_license.text)
access_token = response_json.get('access_token', 'N/A')
account_id = response_json.get('account_id', 'N/A')

headers_content = {
    'authorization': f'Bearer {access_token}',
    'referer': 'https://www.crunchyroll.com/pt-br/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0',
}

params_content = {
    'ratings': 'true',
    'locale': 'pt-BR',
}

response_content = session.get(CRUNCHYROLL_CONTENT_ENDPOINT.format(video_id=video_id), params=params_content, headers=headers_content)
response_data_content = response_content.json()

for data_entry in response_data_content.get('data', []):
    if 'episode_metadata' in data_entry:
        season_number = data_entry['episode_metadata'].get('season_number')
        season_slug_title = data_entry['episode_metadata'].get('season_slug_title')
        season_title = data_entry['episode_metadata'].get('season_title')
        sequence_number = data_entry['episode_metadata'].get('sequence_number')

        print(f"Season Number: {season_number}")
        print(f"Season Slug Title: {season_slug_title}")
        print(f"Season Title: {season_title}")
        print(f"Sequence Number: {sequence_number}")

response_play = requests.get(CRUNCHYROLL_PLAY_ENDPOINT.format(video_id=video_id), headers=headers_content)
video_details = response_play.json()

asset_id = video_details.get('assetId', 'N/A')
token_license_headers = video_details.get('token', 'N/A')
url_mpd = video_details.get('url', 'N/A')
audio_locale = video_details.get('audioLocale', 'N/A')

print(f"audioLocale: {audio_locale}")
print(f"AssetId: {asset_id}")
print(f"Token: {token_license_headers}")
print(f"URL: {url_mpd}")
