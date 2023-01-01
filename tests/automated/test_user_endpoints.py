import unittest

from tests.core_test import TestCore


class TestUserEndpointsSync(unittest.TestCase, TestCore):
    def test_get_bungie_net_user_by_id_sync(self):
        with self.run_test(is_async=False) as client:
            client.user.get_bungie_net_user_by_id(19548659)
            print(f'\tSUCCESS')

    def test_get_sanitized_platform_display_names_sync(self):
        with self.run_test(is_async=False) as client:
            client.user.get_sanitized_platform_display_names(4611686018483530949)
            print(f'\tSUCCESS')

    def test_get_available_themes_sync(self):
        with self.run_test(is_async=False) as client:
            client.user.get_available_themes()
            print(f'\tSUCCESS')


class TestUserEndpointsAsync(unittest.IsolatedAsyncioTestCase, TestCore):
    async def test_get_bungie_net_user_by_id_async(self):
        with self.run_test(is_async=True) as client:
            await client.user.get_bungie_net_user_by_id(19548659)
            print(f'\tSUCCESS')

    async def test_get_sanitized_platform_display_names_async(self):
        with self.run_test(is_async=True) as client:
            await client.user.get_sanitized_platform_display_names(4611686018483530949)
            print(f'\tSUCCESS')

    async def test_get_available_themes_async(self):
        with self.run_test(is_async=True) as client:
            await client.user.get_available_themes()
            print(f'\tSUCCESS')


if __name__ == "__main__":
    unittest.main()
