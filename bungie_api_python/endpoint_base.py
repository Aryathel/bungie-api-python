import abc
from typing import TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .client_sync import BungieClientSync
    from .client_async import BungieClientAsync

    ClientType = TypeVar('ClientType', BungieClientSync, BungieClientAsync)


class EndpointBase(abc.ABC):
    def __init__(self, parent: 'ClientType'):
        self.parent = parent

    def __init_subclass__(
            cls,
            name: str = None,
            api_base: str = None,
            **kwargs
    ) -> None:
        if not api_base:
            raise ValueError(
                "A valid api_base subclass parameter must be passed indicating the API "
                "root url for the endpoint collection."
            )
        if not name:
            name = cls.__name__
        cls.name = name
        cls.api_base = api_base
