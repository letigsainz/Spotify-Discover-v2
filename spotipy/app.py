from flask import Flask, redirect, render_template
from dotenv import load_dotenv
import spotify_requests as r
import helpers as hp
import os

load_dotenv()
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
hp.open_browser()


"""
Home page.
"""
@app.route('/')
def home():
    return render_template('index.html')


"""
Get Authorized by spotify.
"""
@app.route('/get_auth')
def request_auth():
    # Auth flow step 1 - request authorization
    scope = 'user-top-read playlist-modify-public playlist-modify-private user-follow-read'
    return redirect(f'https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={scope}')


"""
Back to app while data is fetched.
"""
@app.route('/callback')
def fetch_data():
    tokens = r.request_tokens()
    artist_ids = r.get_artists(tokens)
    album_ids = r.get_albums(tokens, artist_ids)
    track_uris = r.get_tracks(tokens, album_ids)
    playlist_url = r.add_to_playlist(tokens, track_uris)
    return redirect(playlist_url)


if __name__ == '__main__':
   app.run() # dev mode
