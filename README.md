# Spotify Discover (Full Stack version)

## About The Project
I created this app a few years ago to help keep me up to date with the latest music releases by the artists that I love. It's meant to be run locally, every so often, and allow the user to discover new music.

The app uses the Spotify Web API to access a user's followed artists, check if they've released any new music, and if so, add the tracks to a brand new playlist.

It is currently a modest app with a very simple UI, using [Semantic UI](https://semantic-ui.com/introduction/getting-started.html) for styling. I'll hopefully update to a more robust React app in the near future.

> [!IMPORTANT]
> This app uses Werkzeug's simple development server, rather than an actual web server, so it is not appropriate for production use. 

## Screenshots
![Start Screen](/spotipy/screenshots/start.png)

![Loading Screen](/spotipy/screenshots/loading.png)


## Getting Started

Make sure you have Python3 installed. This project uses version 3.13.

[Register](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/) your application with ``http://127.0.0.1:5000/callback`` as the redirect URI to obtain a client ID and secret.

## Setup

Clone the repository and step inside.

Set up a `.env` file in the project's root directory that looks like this:

```
SPOTIFY_CLIENT_ID= '<your_client_id>'
SPOTIFY_CLIENT_SECRET= '<your_client_secret>'
SPOTIFY_REDIRECT_URI= 'http://127.0.0.1:5000/callback'
SPOTIFY_USER_ID= '<your_spotify_user_id>'
```
The `SPOTIFY_USER_ID` must be the user Id of the user for which you created the app in Spotify's developer portal. You won't be able to create a playlist for another user.

## How To Run

### Running with Docker

If you have Docker installed on your machine, then execute the following command in your terminal:
```
docker compose up
```
Once the container has spun up, then open your browser and navigate to http://127.0.0.1:5000.

### Running without Docker

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

### Play by play

The app will ask you to first authenticate with Spotify, and if successful, it will then prompt you to create your new playlist. You can view the progress inside the terminal's output. 

Once the playlist has been created, you will be redirected to your Spotify library, and more specifically, to your new playlist, so you can start listening!

:grin:

> [!NOTE]
> You will need to manually shut down the server (^C) when the playlist is completed. The Werkzeug built-in shutdown function that was being used to do this automatically, has since been deprecated (To-do: add new shutdown).
