# Spotify Discover (Full Stack version)

## About The Project
This flask app is meant to run locally every month and allow the user to discover new music.

It uses the Spotify Web API to access your followed artists, check if they've released any new music, and if so, add the tracks to a new playlist for that month.

## Screenshots
![Start Screen](/spotipy/screenshots/start.png)

![Loading Screen](/spotipy/screenshots/loading.png)


## Getting Started

Make sure you have Python3 installed.

[Register](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/) your application with ``http://127.0.0.1:5000/callback`` as the redirect URI to obtain a client ID and secret.

## Setup

Clone the repository and step inside.

Set up a `.env` file in the project's root directory that looks like this:

```
SPOTIFY_CLIENT_ID= '<your_client_id>'
SPOTIFY_CLIENT_SECRET= '<your_client_secret>'
SPOTIFY_REDIRECT_URI= 'http://127.0.0.1:5000/callback'
SPOTIFY_USER_ID= '<your_spotify_user_id>'
SECRET_KEY= '<your_secret_key>'
```
The SECRET_KEY is used by flask to keep data safe (i.e. encrypted). You must set the secret key in order to use session in flask, which this project uses.

Create a secret key using the following command. Copy the resulting string into the SECRET_KEY variable in your .env file.
```
$ python -c 'import os; print(os.urandom(16))'

b'_5#y2L"F4Q8z\n\xec]/'
```

## How To Run

Create a virtual environment within your project directory and activate it (not required, but highly recommended)
```
python3 -m venv venv
```
```
source venv/bin/activate
```

Install required packages:
```
pip install -r requirements.txt
```

Start up the server:
```
export FLASK_APP=spotipy/app.py

python -m flask run
```

## Notes

Why would you want to build URLs using the URL reversing function `url_for()` instead of hard-coding them into your templates?

1. Reversing is often more descriptive than hard-coding the URLs.
2. Maintainability -- You can change your URLs in one go instead of needing to remember to manually change hard-coded URLs. 
3. URL building handles escaping of special characters transparently.
4. The generated paths are always absolute, avoiding unexpected behavior of relative paths in browsers.
5. If your application is placed outside the URL root, for example, in /myapplication instead of /, url_for() properly handles that for you.

For example, in `loading.html` we can set the `href="/create_playlist/{{ code }}"` or instead, use `url_for()` like so, `href="{{ url_for('fetch_data', code=code) }}"`.
