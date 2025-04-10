from datetime import time
from functools import wraps
from spotipy.config import logger


def rate_limit_handler(exception_to_check, tries=3):
    def retry_decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            m_tries = tries
            while m_tries > 1:
                try:
                    return func(*args, **kwargs)
                except exception_to_check as e:
                    if e.response is None or e.response.status_code != 429:
                        return
                    limit_reset = e.response.headers.get('x-ratelimit-reset', 6)
                    delay = max(int(limit_reset) - int(time.time()) + 0.5, 0)
                    logger.warning(f'Rate limit reached for url {e.response.request.url}. Retrying in {delay}ms.')
                    m_tries -= 1
            logger.error('Error fetching from Spotify. Too many requests.')
            return func(*args, **kwargs)
        return inner
    return retry_decorator


def bad_token_handler(exception_to_check):
    def retry_decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_to_check as e:
                if e.response is None or e.response.status_code != 401:
                    return
                logger.error('Bad or expired token. Refreshing token...')
                # token = get_token_from_cache()
                token = 'token'  # test
                kwargs['headers'].update({'Authorization': f'Bearer {token}'})
                return func(*args, **kwargs)
        return inner
    return retry_decorator
