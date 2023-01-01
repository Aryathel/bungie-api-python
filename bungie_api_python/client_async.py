# --- IMPORTS ----------------------------------------------------------------------------------------------------------
from contextlib import asynccontextmanager
from typing import TypeVar, Any, Optional, Type, Generator

import aiohttp

from .client_base import ClientBase
from .endpoints import AppEndpointsAsync, OAuthAsync, UserEndpointsAsync
from .entities.core.oauth import AccessToken
from .entities.responses import Response
from .exceptions.oauth import OAuthContextNotFoundException, OAuthContextExpiredException, \
    OAuthContextGenFailedException
from .utils import OAuthUtils

# --- TYPING -----------------------------------------------------------------------------------------------------------
R = TypeVar('R', bound=Response | AccessToken)


# --- CLASSES ----------------------------------------------------------------------------------------------------------
class BungieClientAsync(
    ClientBase,
    endpoints=[
        AppEndpointsAsync,
        OAuthAsync,
        UserEndpointsAsync,
    ],
):
    app: AppEndpointsAsync
    oauth: OAuthAsync
    user: UserEndpointsAsync

    async def oauth_context(self) -> str:
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
                self._access_token = await self.oauth.refresh_access_token(self._access_token.refresh_token)
            except aiohttp.ClientResponseError:
                raise OAuthContextExpiredException(
                    "The previous OAuth context has expired and cannot be refreshed. "
                    "Please reset the oauth context using the client's 'create_oauth_context' or 'set_oauth_context' "
                    "method, then try using this method again."
                )

        return OAuthUtils.access_token_header(self._access_token)

    @asynccontextmanager
    async def session(self, with_oauth: bool) -> Generator[aiohttp.ClientSession, None, None]:
        headers = {
            'X-API-Key': self.api_key,
            'User-Agent': 'bungie-api-python'
        }
        if with_oauth:
            headers.update({
                'Authorization': await self.oauth_context()
            })

        async with aiohttp.ClientSession(
                headers=headers,
                # raise_for_status=True,
        ) as session:
            yield session

    async def get(
            self,
            url: str,
            response_type: Type[R] = Response,
            params: Optional[dict[str, Any]] = None,
            headers: Optional[dict[str, Any]] = None,
            data: Optional[dict[str, Any]] = None,
            requires_oauth: bool = False,
            auth: aiohttp.BasicAuth = None,
    ) -> R:
        async with self.session(with_oauth=requires_oauth) as session:
            async with session.get(
                url,
                headers=headers,
                params=params,
                auth=auth,
                data=data,
            ) as r:
                return response_type.from_dict(await r.json())

    async def post(
            self,
            url: str,
            response_type: Type[R] = Response,
            params: Optional[dict[str, Any]] = None,
            headers: Optional[dict[str, Any]] = None,
            data: Optional[dict[str, Any]] = None,
            requires_oauth: bool = False,
            auth: aiohttp.BasicAuth = None,
    ) -> R:
        async with self.session(with_oauth=requires_oauth) as session:
            async with session.post(
                url,
                headers=headers,
                params=params,
                auth=auth,
                data=data,
            ) as r:
                print(await r.json())
                return response_type.from_dict(await r.json())

    async def gen_oauth_context(
            self,
            code: str
    ) -> None:
        try:
            self._access_token = await self.oauth.get_access_token(code)
        except aiohttp.ClientResponseError:
            raise OAuthContextGenFailedException(f"Failed to create OAuth context with code: {code}.")

    def set_oauth_context(self, access_token: AccessToken) -> None:
        self._access_token = access_token
