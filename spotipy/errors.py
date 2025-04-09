class AuthenticationError(Exception):
    def __init__(self, message="Authentication failed"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

class SpotifyRateLimitReachedException(Exception):
    def __init__(self, response):
        super().__init__()
        self.response = response

class AuthTokenBadOrExpiredException(Exception):
    def __init__(self, response):
        super().__init__()
        self.response = response
