import aiohttp
from requests.auth import HTTPBasicAuth

from ..endpoint_base import EndpointBase
from ..entities.core.enums import OAuthClientType
from ..entities.core.oauth import AccessToken
from ..exceptions.oauth import NonOAuthClientTypeException


class OAuth(EndpointBase, api_base='https://www.bungie.net/Platform/App/OAuth/Token', name='oauth'):
    def get_access_token(self, code: str) -> AccessToken:
        if self.parent.client_type == OAuthClientType.NotApplicable:
            raise NonOAuthClientTypeException(
                f"The provided client type of {self.parent.client_type.name} does not support OAuth endpoints."
            )

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        body = {
            'grant_type': 'authorization_code',
            'code': code,
        }
        auth = None

        if self.parent.client_type == OAuthClientType.Public:
            body.update({'client_id': self.parent.client_id})
        elif self.parent.client_type == OAuthClientType.Confidential:
            auth = HTTPBasicAuth(str(self.parent.client_id), self.parent.client_secret)

        return self.parent.post(
            self.api_base,
            response_type=AccessToken,
            headers=headers,
            data=body,
            auth=auth,
        )

    def refresh_access_token(self, refresh_token: str) -> AccessToken:
        if self.parent.client_type == OAuthClientType.Confidential:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            body = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
            }
            auth = HTTPBasicAuth(str(self.parent.client_id), self.parent.client_secret)

            return self.parent.post(
                self.api_base,
                response_type=AccessToken,
                headers=headers,
                data=body,
                auth=auth,
            )
        else:
            raise NonOAuthClientTypeException(
                f"The provided client type of {self.parent.client_type.name} does not support OAuth "
                f"refresh token endpoints."
            )


class OAuthAsync(EndpointBase, api_base='https://www.bungie.net/Platform/App/OAuth/Token/', name='oauth'):
    async def get_access_token(self, code: str) -> AccessToken:
        if self.parent.client_type == OAuthClientType.NotApplicable:
            raise NonOAuthClientTypeException(
                f"The provided client type of {self.parent.client_type.name} does not support OAuth endpoints."
            )

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        body = {
            'grant_type': 'authorization_code',
            'code': code,
        }
        auth = None

        if self.parent.client_type == OAuthClientType.Public:
            body.update({'client_id': self.parent.client_id})
        elif self.parent.client_type == OAuthClientType.Confidential:
            auth = aiohttp.BasicAuth(str(self.parent.client_id), self.parent.client_secret)

        return await self.parent.post(
            self.api_base,
            response_type=AccessToken,
            headers=headers,
            data=body,
            auth=auth,
        )

    async def refresh_access_token(self, refresh_token: str) -> AccessToken:
        if self.parent.client_type == OAuthClientType.Confidential:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            body = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
            }
            auth = aiohttp.BasicAuth(str(self.parent.client_id), self.parent.client_secret)

            return await self.parent.post(
                self.api_base,
                response_type=AccessToken,
                headers=headers,
                data=body,
                auth=auth,
            )
        else:
            raise NonOAuthClientTypeException(
                f"The provided client type of {self.parent.client_type.name} does not support OAuth "
                f"refresh token endpoints."
            )
