from typing import TypeVar, Any, Optional, Type

import requests

from .client_base import ClientBase


# --- TYPING -----------------------------------------------------
R = TypeVar('R', bound=Response)


class BungieSyncClient(ClientBase):
    def get(
            self,
            url: str,
            response_type: Type[R],
            params: Optional[dict[str, Any]] = None,
            headers: Optional[dict[str, Any]] = None,
    ) -> R:
        if not headers:
            headers = {}
        headers = headers.update({'X-API-Key': self.api_key})

        with requests.Session()
