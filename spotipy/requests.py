import requests
from spotipy.config import logger
# from spotipy.errors import AuthenticationError


def _get(uri, headers, reset_headers=None):
    try:
        response = requests.get(uri, headers)
        response.raise_for_status()
    except requests.HTTPError as e:
        if e.response.status_code == 401:  # bad or expired token
            logger.error('Token error. Retrying request...')
            response = requests.get(uri, headers=reset_headers())
        else:
            logger.error(f'Authentication Error {e}')
            # TO-DO: kick user back to login
    return response.json()

def _post(uri, data, reset_headers=None, headers=None):
    try:
        response = requests.post(uri, data, headers)
        response.raise_for_status()
    except requests.HTTPError as e:
        if e.response.status_code == 401:  # bad or expired token
            logger.error('Token error. Retrying request...')
            response = requests.post(uri, data, headers=reset_headers())
        else:
            logger.error(f'Authentication Error {e}')
            # TO-DO: kick user back to login
    return response.json()
