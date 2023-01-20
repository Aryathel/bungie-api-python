import os
import unittest
from typing import Type

from generated import BungieClientSync, BungieClientAsync


class TestCore(unittest.TestCase):
    _sync_client: BungieClientSync = None
    _async_client: BungieClientAsync = None
    tests: list[str]

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

    @classmethod
    def suite(cls) -> unittest.TestSuite:
        suite = unittest.TestSuite()
        for test in cls.tests:
            suite.addTest(cls(test))
        return suite

    @classmethod
    def run_test(cls) -> None:
        print(f' {cls.__name__.replace("Test", "").upper()} TESTS '.center(100, '='))
        unittest.TextTestRunner().run(cls.suite())
