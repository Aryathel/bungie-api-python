# --- IMPORTS ----------------------------------------------------------------------------------------------------------
from contextlib import asynccontextmanager
from typing import TypeVar, Any, Optional, Type, Generator

import aiohttp

from .client_base import ClientBase
from .endpoints import AppEndpointsAsync
from .entities.responses import Response

# --- TYPING -----------------------------------------------------------------------------------------------------------
R = TypeVar('R', bound=Response)


# --- CLASSES ----------------------------------------------------------------------------------------------------------
class BungieClientAsync(ClientBase, endpoints=[AppEndpointsAsync]):
    app: AppEndpointsAsync

    _session: aiohttp.ClientSession

    @asynccontextmanager
    async def session(self) -> Generator[aiohttp.ClientSession, None, None]:
        async with aiohttp.ClientSession(
                headers={
                    'X-API-Key': self.api_key,
                    'User-Agent': 'bungie-api-python'
                },
                raise_for_status=True
        ) as session:
            yield session

    async def get(
            self,
            url: str,
            response_type: Type[R] = Response,
            params: Optional[dict[str, Any]] = None,
            headers: Optional[dict[str, Any]] = None,
    ) -> R:
        async with self.session() as session:
            async with session.get(url, headers=headers, params=params) as r:
                return response_type.from_dict(await r.json())
