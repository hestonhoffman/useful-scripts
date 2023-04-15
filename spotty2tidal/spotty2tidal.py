#!/usr/bin/python

'''
Turns a Spotify link into a Tidal link.
'''
from dotenv import load_dotenv
import requests, os, re
import tidalapi
import base64
from pprint import pprint

load_dotenv()
TIDAL_TOKEN = os.getenv('TIDAL_TOKEN')
T_REFRESH_TOKEN = os.getenv('T_REFRESH_TOKEN')
SPOTTY_TOKEN = os.getenv('SPOTTY_TOKEN')
SPOTTY_CLIENT_ID = os.getenv('SPOTTY_CLIENT_ID')
encoded_secret = base64.b64encode((SPOTTY_CLIENT_ID + ":" + SPOTTY_TOKEN).encode("ascii")).decode("ascii")

def make_spotty_url(url):
    spotty_url = re.sub('https://open.spotify.com/track/', '', url)
    spotty_url = 'https://api.spotify.com/v1/tracks/' + spotty_url
    return(spotty_url)

spotty_session = requests.Session()
token_url = 'https://accounts.spotify.com/api/token'
headers = {
    'Authorization': f'Basic {encoded_secret}',
    'Content-Type': 'application/x-www-form-urlencoded'}
payload = {'grant_type':'client_credentials'}
get_token = spotty_session.post(url=token_url, headers=headers, data=payload).json()
spotify_token = get_token['access_token']
spotty_session.headers.update({'Authorization': f'Bearer {spotify_token}'})
example_url = 'https://open.spotify.com/track/15irEKZ9D6FQqLoZ1qJ1Cx'
url = make_spotty_url(example_url)
call = spotty_session.get(url)

song = call.json()['name']
artists = call.json()['artists']
for item in artists:
    for entry in item:
        if entry == 'name':
            artist = item[entry]

tsession = tidalapi.Session()
token_type = 'Bearer'
access_token = TIDAL_TOKEN
refresh_token = T_REFRESH_TOKEN

tsession.load_oauth_session(token_type, access_token, refresh_token, tsession.expiry_time)
search_results = tsession.search(song, [tidalapi.media.Track])

for item in search_results['tracks']:
    if artist == item.artist.name:
        print(f'https://tidal.com/browse/track/{item.id}')

    #print(item.artist.name)
    #print(item.id)
    #print(item.album.name)
    #print(item.album.id)
