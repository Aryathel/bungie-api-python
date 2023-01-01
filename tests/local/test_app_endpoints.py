import unittest

from tests.core_test import TestCore

import dotenv

dotenv.load_dotenv()


class TestAppEndpointsSync(unittest.TestCase, TestCore):
    def test_get_application_api_usage_sync(self):
        with self.run_test(is_async=False) as client:
            client.gen_oauth_context(self.oauth_code)

            r = client.app.get_application_api_usage(46374)
            print(f'\tSUCCESS: {r}')

    def test_get_bungie_applications_sync(self):
        with self.run_test(is_async=False) as client:
            r = client.app.get_bungie_applications()
            print(f'\tSUCCESS: {r}')


class TestAppEndpointsAsync(unittest.IsolatedAsyncioTestCase, TestCore):
    async def test_get_application_api_usage_async(self):
        with self.run_test(is_async=True) as client:
            await client.gen_oauth_context(self.oauth_code)

            r = await client.app.get_application_api_usage(46374)
            print(f'\tSUCCESS: {r}')

    async def test_get_bungie_applications_async(self):
        with self.run_test(is_async=True) as client:
            r = await client.app.get_bungie_applications()
            print(f'\tSUCCESS: {r}')


if __name__ == "__main__":
    unittest.main()
