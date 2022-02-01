import webbrowser
import requests
import json

# open browser at address where app is running locally
def open_browser():
    try:
        url = 'http://127.0.0.1:5000/'
        webbrowser.open(url)
    except Exception:
        print('You need to manually open your browser and navigate to: http://127.0.0.1:5000/')

# post request to add tracks to playlist
def add_tracks(tokens, playlist_id, tracks_list):
    uri = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {'Authorization': f'Bearer {tokens["access_token"]}', 'Content-Type': 'application/json'}
    payload = {'uris': tracks_list}
    r = requests.post(uri, headers=headers, data=json.dumps(payload))

# Shut down the flask server
def shutdown_server(environ):
    # look for dev server shutdown function in request environment
    if not 'werkzeug.server.shutdown' in environ:
        raise RuntimeError('Not running the development server')
    environ['werkzeug.server.shutdown']() # call the shutdown function
    print('Shutting down server...')
