import unittest
import os

import bungie_api_python


class TestAppEndpointsSync(unittest.TestCase):
    def test_get_bungie_applications_sync(self):
        api_key = os.getenv("BUNGIE_API_KEY")
        client = bungie_api_python.BungieClientSync(api_key=api_key)

        client.app.get_bungie_applications()


class TestAppEndpointsAsync(unittest.IsolatedAsyncioTestCase):
    async def test_get_bungie_applications_async(self):
        api_key = os.getenv("BUNGIE_API_KEY")
        client = bungie_api_python.BungieClientAsync(api_key=api_key)

        await client.app.get_bungie_applications()


if __name__ == "__main__":
    unittest.main()
