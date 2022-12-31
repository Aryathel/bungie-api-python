# --- IMPORTS ----------------------------------------------------------------------------------------------------------
from contextlib import contextmanager
from typing import TypeVar, Any, Optional, Type, Generator

import requests

from .client_base import ClientBase
from .endpoints import AppEndpoints
from .entities.responses import Response

# --- TYPING -----------------------------------------------------------------------------------------------------------
R = TypeVar('R', bound=Response)


# --- CLASSES ----------------------------------------------------------------------------------------------------------
class BungieClientSync(ClientBase, endpoints=[AppEndpoints]):
    app: AppEndpoints

    _session: requests.Session

    @contextmanager
    def session(self) -> Generator[requests.Session, None, None]:
        if not self._session:
            self._session = requests.Session()
            self._session.headers.update({
                'X-API-Key': self.api_key,
                'User-Agent': 'bungie-api-python'
            })

        yield self._session

    def get(
            self,
            url: str,
            response_type: Type[R] = Response,
            params: Optional[dict[str, Any]] = None,
            headers: Optional[dict[str, Any]] = None,
    ) -> R:
        with self.session() as session:
            r: requests.Response = session.get(url, headers=headers, params=params)
            r.raise_for_status()
            return response_type.from_dict(r.json())
