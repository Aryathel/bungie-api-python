import abc
import os
import sys
from contextlib import contextmanager
from typing import Generator

import dotenv

import bungie_api_python
from bungie_api_python.entities.core.enums import OAuthClientType

dotenv.load_dotenv()


class TestCore(abc.ABC):
    api_key: str
    client_id: int
    client_secret: str
    client_type: OAuthClientType
    oauth_code: str

    _initialized: bool

    def initialize(self):
        if getattr(self, '_initialized', False):
            return
        self.api_key = os.getenv("BUNGIE_API_KEY")
        self.client_id = os.getenv("BUNGIE_CLIENT_ID")
        if self.client_id:
            self.client_id = int(self.client_id)
        self.client_secret = os.getenv("BUNGIE_CLIENT_SECRET")
        self.client_type = os.getenv("BUNGIE_CLIENT_TYPE")
        if self.client_type:
            self.client_type = OAuthClientType(int(self.client_type))
        self.oauth_code = os.getenv("BUNGIE_OAUTH_CODE")
        self._initialized = True

    @contextmanager
    def run_test(self, is_async: bool) -> Generator[bungie_api_python.BungieClientSync | bungie_api_python.BungieClientAsync, None, None]:
        self.initialize()
        print(f'RUNNING TEST: {sys._getframe(2).f_code.co_name}')
        print(f'OAUTH URL: https://www.bungie.net/en/OAuth/Authorize?client_id={self.client_id}&response_type=code')
        if not is_async:
            client = bungie_api_python.BungieClientSync(
                api_key=self.api_key,
                client_id=self.client_id,
                client_secret=self.client_secret,
                client_type=self.client_type,
            )
        else:
            client = bungie_api_python.BungieClientAsync(
                api_key=self.api_key,
                client_id=self.client_id,
                client_secret=self.client_secret,
                client_type=self.client_type,
            )
        yield client
        print('\n')
