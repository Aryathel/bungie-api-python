# --- IMPORTS ----------------------------------------------------------------------------------------------------------
import abc
from contextlib import contextmanager, asynccontextmanager
from typing import Generator, overload, TypeVar, Type, Optional, Any

import requests
from requests.auth import HTTPBasicAuth
import aiohttp

from .endpoint_base import EndpointBase
from .entities.core import AccessToken
from .entities.core.enums import OAuthClientType
from .entities.responses import Response

# --- TYPING -----------------------------------------------------------------------------------------------------------
R = TypeVar('R', bound=Response | AccessToken)
EndpointType = TypeVar('EndpointType', bound=EndpointBase)


# --- ABSTRACT BASE CLASSES --------------------------------------------------------------------------------------------
class ClientBase(abc.ABC):
    """The bottom-most level abstract class that the synchronous and asynchronous
    client implementations both inherit from.

    This class manages connection sessions across the multitude of endpoints in use.
    """
    _endpoints: list[EndpointType]

    api_key: str
    client_id: int
    client_type: OAuthClientType

    _access_token: Optional[AccessToken]

    def __init__(
            self,
            api_key: str,
            client_type: OAuthClientType = OAuthClientType.Public,
            client_id: int = None,
            client_secret: str = None,
    ) -> None:
        """Instantiates the client class and all endpoint classes.

        :param api_key: The Bungie API key that will be used when making requests.
        """
        self.api_key = api_key
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_type = client_type

        self._session = None
        self._access_token = None

        for endpoint in self._endpoints:
            setattr(self, endpoint.name, endpoint(self))

    def __init_subclass__(cls, endpoints: list[EndpointType] = None, **kwargs) -> None:
        """Links any endpoint groups to the parent client at runtime.

        :param endpoints: The endpoint classes to connect to this parent client.
        """
        if not endpoints:
            raise ValueError(
                "At least one endpoint collection must be provided for the client to function."
            )
        cls._endpoints = endpoints

    @abc.abstractmethod
    @overload
    @asynccontextmanager
    async def session(self, with_oauth: bool) -> Generator[aiohttp.ClientSession, None, None]:
        ...

    @abc.abstractmethod
    @contextmanager
    def session(self, with_oauth: bool) -> Generator[requests.Session, None, None]:
        pass

    @abc.abstractmethod
    @overload
    async def get(
            self,
            url: str,
            response_type: Type[R] = Response,
            params: Optional[dict[str, Any]] = None,
            headers: Optional[dict[str, Any]] = None,
            data: Optional[dict[str, Any]] = None,
            json: Optional[dict[str, any]] = None,
            requires_oauth: bool = False,
            auth: aiohttp.BasicAuth = None,
    ) -> R:
        ...

    @abc.abstractmethod
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
        pass

    @abc.abstractmethod
    @overload
    async def post(
            self,
            url: str,
            response_type: Type[R] = Response,
            params: Optional[dict[str, Any]] = None,
            headers: Optional[dict[str, Any]] = None,
            data: Optional[dict[str, Any]] = None,
            json: Optional[dict[str, any]] = None,
            requires_oauth: bool = False,
            auth: aiohttp.BasicAuth = None,
    ) -> R:
        ...

    @abc.abstractmethod
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
        pass

    @abc.abstractmethod
    @overload
    async def gen_oauth_context(
            self,
            code: str
    ) -> None:
        ...

    @abc.abstractmethod
    def gen_oauth_context(
            self,
            code: str
    ) -> None:
        pass

    @abc.abstractmethod
    @overload
    async def set_oauth_context(
            self,
            access_token: AccessToken
    ) -> None:
        ...

    @abc.abstractmethod
    def set_oauth_context(
            self,
            access_token: AccessToken
    ) -> None:
        pass

