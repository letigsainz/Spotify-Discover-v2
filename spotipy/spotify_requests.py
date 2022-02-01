from datetime import datetime, timedelta, date
from flask import request, session
from dotenv import load_dotenv
import helpers as hp
import numpy as np
import requests
import json
import os


load_dotenv() # load environment variables

# client info
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI') # redirect to after granting user permission
USER_ID = os.getenv('SPOTIFY_USER_ID')


# Request Access Tokens
def request_tokens():
    code = request.args.get('code')
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    r = requests.post('https://accounts.spotify.com/api/token', data=payload)
    response = r.json()
    print(f'{r.status_code} - Successfully completed Auth flow!')
    return response


# Get user's followed artists
def get_artists(tokens):
    headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
    r = requests.get('https://api.spotify.com/v1/me/following?type=artist', headers=headers)
    response = r.json()

    artist_ids = []
    artists = response['artists']['items']
    for artist in artists:
        artist_ids.append(artist['id'])

    # While next results page exists, get it and its artist_ids
    while response['artists']['next']:
        next_page_uri = response['artists']['next']
        r = requests.get(next_page_uri, headers=headers)
        response = r.json()
        for artist in response['artists']['items']:
            artist_ids.append(artist['id'])

    print('Retrieved artist IDs!')
    return artist_ids


# Get all albums by followed artists (albums, singles)
def get_albums(tokens, artist_ids):
    album_ids = []
    album_names = {} # used to check for duplicates with different id's * issue with some albums

    # set time frame for new releases (4 weeks)
    today = datetime.now()
    number_weeks = timedelta(weeks=4)
    time_frame = (today - number_weeks).date()

    for id in artist_ids:
        uri = f'https://api.spotify.com/v1/artists/{id}/albums?include_groups=album,single&country=US'
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        r = requests.get(uri, headers=headers)
        response = r.json()

        albums = response['items']
        for album in albums:
            # check for tracks that are new releases (4 weeks)
            try:
                release_date = datetime.strptime(album['release_date'], '%Y-%m-%d') # convert release_date string to datetime
                album_name = album['name']
                artist_name = album['artists'][0]['name']
                if release_date.date() > time_frame:
                    # if we do find a duplicate album name, check if it's by a different artist
                    if album_name not in album_names or artist_name != album_names[album_name]:
                        album_ids.append(album['id'])
                        album_names[album_name] = artist_name
            except ValueError:
                # there appear to be some older release dates that only contain year (2007) - irrelevant
                print(f'Release date found with format: {album["release_date"]}')

    print('Retrieved album IDs!')
    return album_ids


# Get each individual "album's" track uri's
def get_tracks(tokens, album_ids):
    track_uris = []

    for id in album_ids:
        uri = f'https://api.spotify.com/v1/albums/{id}/tracks'
        headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
        r = requests.get(uri, headers=headers)
        response = r.json()

        for track in response['items']:
            track_uris.append(track['uri'])

    print('Retrieved tracks!')
    return track_uris


# Create a new playlist in user account
def create_playlist(tokens, user_id=USER_ID):
    current_date = (date.today()).strftime('%m-%d-%Y')
    playlist_name = f'New Monthly Releases - {current_date}'

    # make request to create_playlist endpoint
    uri = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    headers = {'Authorization': f'Bearer {tokens["access_token"]}', 'Content-Type': 'application/json'}
    payload = {'name': playlist_name}
    r = requests.post(uri, headers=headers, data=json.dumps(payload))
    response = r.json()

    session['playlist_id'] = response['id'] # store our new playlist's id
    session['playlist_url'] = response['external_urls']['spotify'] # store new playlist's url

    print(f'{r.status_code} - Created playlist!')
    return session['playlist_id']


# Add new music releases to our newly created playlist
def add_to_playlist(tokens, track_uris):
    playlist_id = create_playlist(tokens)

    # split up the request if number of tracks is too big. Spotify API max 100 per req.
    number_of_tracks = len(track_uris)

    # split track_uris list into 3 sub lists
    if number_of_tracks > 200:
        three_split = np.array_split(track_uris, 3)
        for lst in three_split:
            hp.add_tracks(tokens, playlist_id, list(lst))

    # split track_uris list into 2 sub lists
    elif number_of_tracks > 100:
        two_split = np.array_split(track_uris, 2)
        for lst in two_split:
            hp.add_tracks(tokens, playlist_id, list(lst))

    else:
        hp.add_tracks(tokens, playlist_id, track_uris)

    print('Added tracks to playlist!')
    # redirect to playlsit page & shut down flask server
    hp.shutdown_server(request.environ)
    return session['playlist_url']
