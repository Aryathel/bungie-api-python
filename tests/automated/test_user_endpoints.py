import unittest

from bungie_api_python.exceptions.core import ObsoleteEndpoint
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

    def test_get_membership_data_by_id_sync(self):
        with self.run_test(is_async=False) as client:
            client.user.get_membership_data_by_id(
                membership_id=4611686018483530949,
                membership_type=3,
            )
            print(f'\tSUCCESS')

    def test_get_membership_from_hard_linked_credential_sync(self):
        with self.run_test(is_async=False) as client:
            client.user.get_membership_from_hard_linked_credential(
                credential_type='SteamId',
                credential=76561198119241330,
            )
            print(f'\tSUCCESS')

    def test_search_by_global_name_prefix_sync(self):
        with self.run_test(is_async=False) as client:
            try:
                client.user.search_by_global_name_prefix('test', 1)
            except Exception as e:
                assert isinstance(e, ObsoleteEndpoint)
                print(f'\tSUCCESS')

    def test_search_by_global_name_post_sync(self):
        with self.run_test(is_async=False) as client:
            client.user.search_by_global_name_post('Mara', 0)
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

    async def test_get_membership_data_by_id_async(self):
        with self.run_test(is_async=True) as client:
            await client.user.get_membership_data_by_id(
                membership_id=4611686018483530949,
                membership_type=3,
            )
            print(f'\tSUCCESS')

    async def test_get_membership_from_hard_linked_credential_async(self):
        with self.run_test(is_async=True) as client:
            await client.user.get_membership_from_hard_linked_credential(
                credential_type='SteamId',
                credential=76561198119241330,
            )
            print(f'\tSUCCESS')

    async def test_search_by_global_name_prefix_async(self):
        with self.run_test(is_async=True) as client:
            try:
                await client.user.search_by_global_name_prefix('test', 1)
            except Exception as e:
                assert isinstance(e, ObsoleteEndpoint)
                print(f'\tSUCCESS')

    async def test_search_by_global_name_post_async(self):
        with self.run_test(is_async=True) as client:
            await client.user.search_by_global_name_post('Mara', 0)
            print(f'\tSUCCESS')


if __name__ == "__main__":
    unittest.main()
