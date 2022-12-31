# --- IMPORTS ----------------------------------------------------------------------------------------------------------
import abc
from contextlib import contextmanager, asynccontextmanager
from typing import Generator, overload, TypeVar, Type, Optional, Any

import requests
import aiohttp

from .endpoint_base import EndpointBase
from .entities.responses import Response

# --- TYPING -----------------------------------------------------------------------------------------------------------
R = TypeVar('R', bound=Response)
SessionType = TypeVar('SessionType', requests.Session, aiohttp.ClientSession)
EndpointType = TypeVar('EndpointType', bound=EndpointBase)


# --- ABSTRACT BASE CLASSES --------------------------------------------------------------------------------------------
class ClientBase(abc.ABC):
    """The bottom-most level abstract class that the synchronous and asynchronous
    client implementations both inherit from.

    This class manages connection sessions across the multitude of endpoints in use.
    """
    endpoints: list[EndpointType]
    api_key: str
    _session: Optional[SessionType]

    def __init__(self, api_key: str) -> None:
        """Instantiates the client class and all endpoint classes.

        :param api_key: The Bungie API key that will be used when making requests.
        """
        self.api_key = api_key
        self._session = None

        for endpoint in self.endpoints:
            setattr(self, endpoint.name, endpoint(self))

    def __init_subclass__(cls, endpoints: list[EndpointType] = None, **kwargs) -> None:
        """Links any endpoint groups to the parent client at runtime.

        :param endpoints: The endpoint classes to connect to this parent client.
        """
        if not endpoints:
            raise ValueError(
                "At least one endpoint collection must be provided for the client to function."
            )
        cls.endpoints = endpoints

    @abc.abstractmethod
    @overload
    @asynccontextmanager
    async def session(self) -> Generator[aiohttp.ClientSession, None, None]:
        ...

    @abc.abstractmethod
    @contextmanager
    def session(self) -> Generator[requests.Session, None, None]:
        pass

    @abc.abstractmethod
    @overload
    async def get(
            self,
            url: str,
            response_type: Type[R] = Response,
            params: Optional[dict[str, Any]] = None,
            headers: Optional[dict[str, Any]] = None,
    ) -> R:
        ...

    @abc.abstractmethod
    def get(
            self,
            url: str,
            response_type: Type[R] = Response,
            params: Optional[dict[str, Any]] = None,
            headers: Optional[dict[str, Any]] = None,
    ) -> R:
        pass

