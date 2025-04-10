import requests
from spotipy.decorators import bad_token_handler, rate_limit_handler
from spotipy.errors import AuthTokenBadOrExpiredException, SpotifyRateLimitReachedException


def check_rate_limit(response):
    if response.status_code == 429:
        raise SpotifyRateLimitReachedException(response=response)

def check_bad_token(response):
    if response.status_code == 401:
        raise AuthTokenBadOrExpiredException(response=response)

@rate_limit_handler(exception_to_check=SpotifyRateLimitReachedException)
@bad_token_handler(exception_to_check=AuthTokenBadOrExpiredException)
def request(method, url, headers, params=None, data=None):
    response = requests.request(method=method, url=url, headers=headers, params=params, data=data)
    check_rate_limit(response)
    check_bad_token(response)
    return response.json()

def get(url, headers, params=None):
    return request('GET', url=url, headers=headers, params=params)

def post(url, headers, data=None):
    return request('POST', url=url, headers=headers, data=data)
