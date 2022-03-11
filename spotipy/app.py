from flask import Flask, redirect, render_template, request
from spotify_client import SpotifyClient
from dotenv import load_dotenv
import helpers as hp
import os

load_dotenv()
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
hp.open_browser()


@app.route('/')
def home():
    """Homepage"""
    return render_template('index.html')


@app.route('/get_auth')
def request_auth():
    """Request user authorization from spotify."""
    scope = 'user-top-read playlist-modify-public playlist-modify-private user-follow-read'
    return redirect(f'https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={scope}')


@app.route('/callback')
def load_page():
    """Back to app after user signs in. User can now create playlist."""
    if request.args.get('error'):
        error_msg = request.args.get('error')
        raise ValueError(error_msg)

    code = request.args.get('code')
    return render_template('loading.html', code=code)


@app.route('/create_playlist/<code>')
def fetch_data(code):
    """Fetch data for new playlist."""
    client = SpotifyClient(
        CLIENT_ID,
        CLIENT_SECRET,
        REDIRECT_URI
    )
    client.request_api_tokens(code)

    artist_ids = client.get_artists()
    album_ids = client.get_albums(artist_ids)
    track_uris = client.get_tracks(album_ids)
    playlist_url = client.add_to_playlist(track_uris)

    return redirect(playlist_url)


if __name__ == '__main__':
    app.run()  # dev mode
