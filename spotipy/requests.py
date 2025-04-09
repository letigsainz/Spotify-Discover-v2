import requests
from spotipy.decorators import bad_token_handler, rate_limit_handler
from spotipy.errors import AuthTokenBadOrExpiredException, SpotifyRateLimitReachedException
from spotipy.config import logger


# def request(method, url, headers=None, params=None, data=None):
#     response = requests.request(method=method, url=url, headers=headers, params=params, data=data)

#     if response.status_code == 401:
#         logger.warning('Bad or expired token. Refreshing tokens...')
#         pass  # working on decorator function TO-DO
#     return response.json()

# def get(url, params=None, headers=None):
#     return request('GET', url=url, headers=headers, params=params)

# def post(url, data=None, headers=None, code_exchange=None):
#     return request('POST', url=url, headers=headers, data=data, code_exchange=code_exchange)


##################
# Work in progress -
# updating request methods to use decorator functions checking for 401,429
##################

def check_rate_limit(response):
    if response.status_code == 429:
        raise SpotifyRateLimitReachedException(response=response)
    
def check_bad_token(response):
    if response.status_code == 401:
        raise AuthTokenBadOrExpiredException(response=response)

@rate_limit_handler(exception_to_check=SpotifyRateLimitReachedException)
@bad_token_handler(exception_to_check=AuthTokenBadOrExpiredException)
def request(method, url, headers=None, params=None, data=None, code_exchange=None):
    # if code_exchange != True:
    #     bearer_token = session['access_token']
    #     headers = {**(headers or {}), **{'Authorization': bearer_token}}
    response = requests.request(method=method, url=url, headers=headers, params=params, data=data)
    check_rate_limit(response)
    check_bad_token(response)
    return response

def get(url, params=None, headers=None):
    return request('GET', url=url, headers=headers, params=params)

def post(url, data=None, headers=None, code_exchange=None):
    return request('POST', url=url, headers=headers, data=data, code_exchange=code_exchange)
