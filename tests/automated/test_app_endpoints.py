import unittest

from tests.core_test import TestCore


class TestAppEndpointsSync(unittest.TestCase, TestCore):
    def test_get_application_api_usage_sync(self):
        with self.run_test(is_async=False) as client:
            r = client.app.get_bungie_applications()
            print(f'\tSUCCESS')


class TestAppEndpointsAsync(unittest.IsolatedAsyncioTestCase, TestCore):
    async def test_get_bungie_applications_async(self):
        with self.run_test(is_async=True) as client:
            await client.app.get_bungie_applications()
            print(f'\tSUCCESS')


if __name__ == "__main__":
    unittest.main()
