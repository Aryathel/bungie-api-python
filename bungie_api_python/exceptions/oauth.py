class OAuthException(Exception):
    pass


class OAuthContextNotFoundException(OAuthException):
    pass


class OAuthContextExpiredException(OAuthException):
    pass


class OAuthContextGenFailedException(OAuthException):
    pass


class NonOAuthClientTypeException(OAuthException):
    pass
