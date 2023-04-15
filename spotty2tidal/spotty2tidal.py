#!/usr/bin/python

'''
Turns a Spotify link into a Tidal link.
'''

import os
import re
import base64
from argparse import ArgumentParser
import requests
import tidalapi
from dotenv import load_dotenv

load_dotenv()
TIDAL_TOKEN = os.getenv('TIDAL_TOKEN')
T_REFRESH_TOKEN = os.getenv('T_REFRESH_TOKEN')
SPOTTY_TOKEN = os.getenv('SPOTTY_TOKEN')
SPOTTY_CLIENT_ID = os.getenv('SPOTTY_CLIENT_ID')
encoded_secret = base64.b64encode(
        (SPOTTY_CLIENT_ID + ":" + SPOTTY_TOKEN).encode("ascii")
    ).decode("ascii")

def make_spotty_url(url):
    '''Create a Spotify endpoint for the track'''
    spotty_url = re.sub('https://open.spotify.com/track/', '', url)
    spotty_url = 'https://api.spotify.com/v1/tracks/' + spotty_url
    return spotty_url


def get_track_details(user_url):
    '''Grab track name and artist metadata from Spotify'''
    spotty_session = requests.Session()
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': f'Basic {encoded_secret}',
        'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'grant_type':'client_credentials'}
    get_token = spotty_session.post(url=token_url, headers=headers, data=payload).json()
    spotify_token = get_token['access_token']
    spotty_session.headers.update({'Authorization': f'Bearer {spotify_token}'})
    url = make_spotty_url(user_url)
    call = spotty_session.get(url)
    song = call.json()['name']
    spotify_artists = []
    artists = call.json()['artists']
    for item in artists:
        for entry in item:
            if entry == 'name':
                spotify_artists.append(item[entry])
    return song, spotify_artists

def match_tidal_track(spotify_song, spotify_artists):
    '''Use Spotify data to match and find the Tidal URL'''
    tsession = tidalapi.Session()
    token_type = 'Bearer'
    access_token = TIDAL_TOKEN
    refresh_token = T_REFRESH_TOKEN

    tsession.load_oauth_session(token_type, access_token, refresh_token, tsession.expiry_time)
    search_results = tsession.search(spotify_song, [tidalapi.media.Track])
    for item in search_results['tracks']:
        print(f"Track name: {item.name}, Artist Name: {item.artist.name}")
        for tidal_artist in item.artists:
            if tidal_artist.name in tuple(spotify_artists):
                return f'https://tidal.com/browse/track/{item.id}'
    return 'No match found'
parser = ArgumentParser()
parser.add_argument('user_url')
args = parser.parse_args()
song, artists = get_track_details(args.user_url)
tidal_url = match_tidal_track(song, artists)
print(tidal_url)
