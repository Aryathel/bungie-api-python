import os

from generated import BungieClientSync, BungieClientAsync


class TestCore:
    _sync_client: BungieClientSync = None
    _async_client: BungieClientAsync = None

    @property
    def sync_client(self) -> BungieClientSync:
        if not self._sync_client:
            self._sync_client = BungieClientSync(
                os.getenv('BUNGIE_API_KEY'),
                os.getenv('BUNGIE_CLIENT_ID'),
                os.getenv('BUNGIE_CLIENT_SECRET'),
            )
        return self._sync_client

    @property
    def async_client(self) -> BungieClientAsync:
        if not self._async_client:
            self._async_client = BungieClientAsync(
                os.getenv('BUNGIE_API_KEY'),
                os.getenv('BUNGIE_CLIENT_ID'),
                os.getenv('BUNGIE_CLIENT_SECRET'),
            )
        return self._async_client
