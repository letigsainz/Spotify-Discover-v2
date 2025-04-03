from datetime import datetime, timedelta, date
import logging
from flask import session
from spotipy.cache import TokenCache
import numpy as np
import json
import os
from spotipy.errors import AuthenticationError
from spotipy.requests import _get, _post

logger = logging.getLogger(__name__)


class SpotifyClient:


    def __init__(self, client_id, client_secret, redirect_uri):
        self.CACHE = TokenCache()
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.headers = {}

    def request_api_tokens(self, code):
        """Request access and refresh tokens"""
        if code is None:
            raise AuthenticationError('No authorization code found.')
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        content = _post('https://accounts.spotify.com/api/token', data=payload)
        self.save_token_to_cache(content.get('access_token'), content.get('refresh_token'), content.get('expires_in'))
        logger.info('Successfully completed auth flow!')

        return content


    def save_token_to_cache(self, access_token, refresh_token, expires_in):
        self.CACHE.save_token('access_token', access_token, expires_in)
        self.CACHE.save_token('refresh_token', refresh_token, 8600)  # save 'forever'
        logger.info('Saved tokens to cache.')


    def get_token_from_cache(self):
        """Retrieve the token from cache"""
        cached_token = self.CACHE.get_token('access_token')
        if not cached_token:
            cached_refresh_token = self.CACHE.get_token('refresh_token')
            if not cached_refresh_token:
                logger.error('No refresh token available. Logging the user out...')
                raise AuthenticationError('Refresh token missing.')
            return self.refresh_tokens(cached_refresh_token)
        return cached_token


    def refresh_tokens(self, refresh_token):
        """Refresh access token"""
        pass


    def set_request_headers(self):
        """Prep request headers with access token"""
        access_token = self.get_token_from_cache()
        self.headers = {'Authorization': f'Bearer {access_token}'}
        return self.headers


    def get_artists(self):
        """Get current user's followed artists"""
        content = _get('https://api.spotify.com/v1/me/following?type=artist', headers=self.headers, reset_headers=self.set_request_headers)
        artist_ids = []
        artists = content['artists']['items']
        for artist in artists:
            artist_ids.append(artist['id'])

        # While next results page exists, get it and its artist_ids
        while content['artists']['next']:
            next_page_uri = content['artists']['next']
            content = _get(next_page_uri, headers=self.headers, reset_headers=self.set_request_headers)

            for artist in content['artists']['items']:
                artist_ids.append(artist['id'])

        logger.info('Retrieved artist IDs!')
        return artist_ids


    def get_albums(self, artist_ids):
        """Get all albums by followed artists (albums, singles)"""
        album_ids = []
        album_names = {}  # used to check for duplicates with different id's * issue with some albums

        # set time frame for new releases (4 weeks)
        today = datetime.now()
        number_weeks = timedelta(weeks=4)
        time_frame = (today - number_weeks).date()

        for id in artist_ids:
            uri = f'https://api.spotify.com/v1/artists/{id}/albums?include_groups=album,single&country=US'
            content = _get(uri, headers=self.headers, reset_headers=self.set_request_headers)

            albums = content['items']
            for album in albums:
                # check for new releases
                try:
                    release_date = datetime.strptime(album['release_date'], '%Y-%m-%d')
                    album_name = album['name']
                    artist_name = album['artists'][0]['name']
                    if release_date.date() > time_frame:
                        # if we do find a duplicate album name, check if it's by a different artist
                        if album_name not in album_names or artist_name != album_names[album_name]:
                            album_ids.append(album['id'])
                            album_names[album_name] = artist_name
                except ValueError:
                    # there appear to be some older release dates that only contain year (2007) - irrelevant
                    logger.info(f'Release date found with format: {album["release_date"]}')

        logger.info('Retrieved album IDs!')
        return album_ids


    def get_tracks(self, album_ids):
        """Get each individual album's track uri's"""
        track_uris = []
        for id in album_ids:
            uri = f'https://api.spotify.com/v1/albums/{id}/tracks'
            content = _get(uri, headers=self.headers, reset_headers=self.set_request_headers)

            for track in content['items']:
                track_uris.append(track['uri'])

        logger.info('Retrieved tracks!')
        return track_uris


    def create_playlist(self, user_id=os.getenv('SPOTIFY_USER_ID')):
        """Create a new playlist in user's account"""
        current_date = (date.today()).strftime('%m-%d-%Y')
        playlist_name = f'New Monthly Releases - {current_date}'

        uri = f'https://api.spotify.com/v1/users/{user_id}/playlists'
        payload = {'name': playlist_name}
        content = _post(uri, headers=self.headers, reset_headers=self.set_request_headers, data=json.dumps(payload))

        session['playlist_id'] = content['id']  # store new playlist's id
        session['playlist_url'] = content['external_urls']['spotify']  # store new playlist's url

        logger.info('Created playlist!')
        return session['playlist_id']


    def add_to_playlist(self, track_uris):
        """Add new music releases to our newly created playlist"""
        playlist_id = self.create_playlist()
        number_of_tracks = len(track_uris)  # Spotify API limit - max 100 tracks per req.

        if number_of_tracks > 200:
            three_split = np.array_split(track_uris, 3)
            for lst in three_split:
                self.add_tracks(self.headers, playlist_id, list(lst))
        elif number_of_tracks > 100:
            two_split = np.array_split(track_uris, 2)
            for lst in two_split:
                self.add_tracks(self.headers, playlist_id, list(lst))
        else:
            self.add_tracks(self.headers, playlist_id, track_uris)

        logger.info('Added tracks to playlist!')
        # hp.shutdown_server(request.environ)  # deprecated, will change for another way to shutdown
        return session['playlist_url']


    def add_tracks(self, headers, playlist_id, tracks_list):
        """Add some number of tracks to a playlist"""
        uri = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        headers['Content-Type'] = 'application/json'
        payload = {'uris': tracks_list}
        _post(uri, headers=headers, reset_headers=self.set_request_headers, data=json.dumps(payload))
