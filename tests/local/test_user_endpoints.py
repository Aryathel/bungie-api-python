import unittest
import sys
from contextlib import contextmanager
from typing import Generator

import dotenv

import bungie_api_python
from tests.core_test import TestCore

dotenv.load_dotenv()


class TestUserEndpointsSync(unittest.TestCase, TestCore):
    def test_get_bungie_net_user_by_id_sync(self):
        with self.run_test(is_async=False) as client:
            r = client.user.get_bungie_net_user_by_id(19548659)
            print(r)

    def test_get_sanitized_platform_display_names_sync(self):
        with self.run_test(is_async=False) as client:
            r = client.user.get_sanitized_platform_display_names(4611686018483530949)
            print(r)

    def test_get_credential_types_for_target_account_sync(self):
        with self.run_test(is_async=False) as client:
            client.gen_oauth_context(self.oauth_code)
            r = client.user.get_credential_types_for_target_account(4611686018483530949)
            print(r)


class TestUserEndpointsAsync(unittest.IsolatedAsyncioTestCase, TestCore):
    async def test_get_bungie_net_user_by_id_async(self):
        with self.run_test(is_async=True) as client:
            r = await client.user.get_bungie_net_user_by_id(19548659)
            print(r)

    async def test_get_sanitized_platform_display_names_async(self):
        with self.run_test(is_async=True) as client:
            r = await client.user.get_sanitized_platform_display_names(4611686018483530949)
            print(r)

    async def test_get_credential_types_for_target_account_async(self):
        with self.run_test(is_async=True) as client:
            await client.gen_oauth_context(self.oauth_code)
            r = await client.user.get_credential_types_for_target_account(4611686018483530949)
            print(r)


if __name__ == '__main__':
    unittest.main()
