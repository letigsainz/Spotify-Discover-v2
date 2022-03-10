import webbrowser
import requests
import json

# open app locally
def open_browser():
    try:
        url = 'http://127.0.0.1:5000/'
        webbrowser.open(url)
    except Exception:
        print('You need to manually open your browser and navigate to: http://127.0.0.1:5000/')

# Shut down the flask server
def shutdown_server(environ):
    if 'werkzeug.server.shutdown' not in environ:
        raise RuntimeError('Not running the development server')
    environ['werkzeug.server.shutdown']()  # call the shutdown function
    print('Shutting down server...')

# post request to add tracks to playlist
def add_tracks(headers, playlist_id, tracks_list):
    uri = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers['Content-Type'] = 'application/json'
    payload = {'uris': tracks_list}
    requests.post(uri, headers=headers, data=json.dumps(payload))
