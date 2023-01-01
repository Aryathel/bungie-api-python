# --- IMPORTS ----------------------------------------------------------------------------------------------------------
import abc
from contextlib import contextmanager
from typing import TypeVar, Any, Optional, Type, Generator, overload

import requests
from requests.auth import HTTPBasicAuth

from .client_base import ClientBase
from .endpoints import AppEndpoints, OAuth, UserEndpoints
from .entities.core.oauth import AccessToken
from .entities.responses import Response
from .utils import OAuthUtils
from .exceptions.oauth import OAuthContextNotFoundException, OAuthContextExpiredException, \
    OAuthContextGenFailedException

# --- TYPING -----------------------------------------------------------------------------------------------------------
R = TypeVar('R', bound=Response | AccessToken)


# --- CLASSES ----------------------------------------------------------------------------------------------------------
class BungieClientSync(
    ClientBase,
    endpoints=[
        AppEndpoints,
        OAuth,
        UserEndpoints,
    ],
):
    @abc.abstractmethod
    @overload
    async def set_oauth_context(
            self,
            access_token: AccessToken
    ) -> None:
        ...

    app: AppEndpoints
    oauth: OAuth
    user: UserEndpoints

    def oauth_context(self) -> str:
        # OAuth access token not set.
        if self._access_token is None:
            raise OAuthContextNotFoundException(
                "No OAuth context was found."
                "Try using the client's 'create_oauth_context' or 'set_oauth_context' method, "
                "then try using this method again."
            )

        # OAuth access token is expired.
        if OAuthUtils.is_token_expired(self._access_token):
            # OAuth refresh token is expired
            if OAuthUtils.is_refresh_token_expired(self._access_token):
                raise OAuthContextExpiredException(
                    "The previous OAuth context has expired and cannot be refreshed. "
                    "Please reset the oauth context using the client's 'create_oauth_context' or 'set_oauth_context' "
                    "method, then try using this method again."
                )

            # Attempt automatic token refresh
            try:
                self._access_token = self.oauth.refresh_access_token(self._access_token.refresh_token)
            except requests.HTTPError:
                raise OAuthContextExpiredException(
                    "The previous OAuth context has expired and cannot be refreshed. "
                    "Please reset the oauth context using the client's 'create_oauth_context' or 'set_oauth_context' "
                    "method, then try using this method again."
                )

        return OAuthUtils.access_token_header(self._access_token)

    @contextmanager
    def session(self, with_oauth: bool) -> Generator[requests.Session, None, None]:
        with requests.Session() as session:
            session.headers.update({
                'X-API-Key': self.api_key,
                'User-Agent': 'bungie-api-python'
            })
            if with_oauth:
                session.headers.update({
                    'Authorization': self.oauth_context()
                })

            yield session

    def get(
            self,
            url: str,
            response_type: Type[R] = Response,
            params: Optional[dict[str, Any]] = None,
            headers: Optional[dict[str, Any]] = None,
            data: Optional[dict[str, Any]] = None,
            json: Optional[dict[str, any]] = None,
            requires_oauth: bool = False,
            auth: HTTPBasicAuth = None,
    ) -> R:
        with self.session(with_oauth=requires_oauth) as session:
            r: requests.Response = session.get(
                url,
                headers=headers,
                params=params,
                auth=auth,
                data=data,
                json=json,
            )
            r.raise_for_status()
            return response_type.from_dict(r.json())

    def post(
            self,
            url: str,
            response_type: Type[R] = Response,
            params: Optional[dict[str, Any]] = None,
            headers: Optional[dict[str, Any]] = None,
            data: Optional[dict[str, Any]] = None,
            json: Optional[dict[str, any]] = None,
            requires_oauth: bool = False,
            auth: HTTPBasicAuth = None,
    ) -> R:
        with self.session(with_oauth=requires_oauth) as session:
            r: requests.Response = session.post(
                url,
                headers=headers,
                params=params,
                auth=auth,
                data=data,
                json=json,
            )
            r.raise_for_status()
            return response_type.from_dict(r.json())

    def gen_oauth_context(
            self,
            code: str
    ) -> None:
        try:
            self._access_token = self.oauth.get_access_token(code)
        except requests.HTTPError:
            raise OAuthContextGenFailedException(f"Failed to create OAuth context with code: {code}.")

    def set_oauth_context(self, access_token: AccessToken) -> None:
        self._access_token = access_token
