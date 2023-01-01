from datetime import datetime, timedelta
from functools import wraps
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..endpoint_base import EndpointBase
    from ..entities.core import AccessToken


class OAuthUtils:
    @staticmethod
    def access_token_expire_date_utc(access_token: 'AccessToken') -> datetime:
        return datetime.utcnow() + timedelta(seconds=access_token.expires_in)

    @staticmethod
    def refresh_token_expire_date_utc(access_token: 'AccessToken') -> datetime:
        return datetime.utcnow() + timedelta(seconds=access_token.refresh_expires_in)

    @staticmethod
    def access_token_header(access_token: 'AccessToken') -> str:
        return f'{access_token.token_type} {access_token.access_token}'

    @staticmethod
    def is_token_expired(access_token: 'AccessToken') -> bool:
        if access_token.expires_at:
            return datetime.utcnow() >= access_token.expires_at
        else:
            return True

    @staticmethod
    def is_refresh_token_expired(access_token: 'AccessToken') -> bool:
        if access_token.refresh_expires_at:
            return datetime.utcnow() >= access_token.refresh_expires_at
        else:
            return True

