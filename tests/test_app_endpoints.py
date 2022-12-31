import unittest
import os

import dotenv

import bungie_api_python

dotenv.load_dotenv()

BUNGIE_ROOT = "https://bungie.net/Platform"


class TestAppEndpointsSync(unittest.TestCase):
    def test_get_bungie_applications_sync(self):
        api_key = os.getenv("BUNGIE_API_KEY")
        print("Running Test With API KEY:", api_key)
        client = bungie_api_python.BungieClientSync(api_key=api_key)

        r = client.app.get_bungie_applications()
        for app in r.Response:
            print(f'{app.name}: {app.status}')


class TestAppEndpointsAsync(unittest.IsolatedAsyncioTestCase):
    async def test_get_bungie_applications_async(self):
        api_key = os.getenv("BUNGIE_API_KEY")
        print("Running Test With API KEY:", api_key)
        client = bungie_api_python.BungieClientAsync(api_key=api_key)

        r = await client.app.get_bungie_applications()
        for app in r.Response:
            print(f'{app.name}: {app.status}')


if __name__ == "__main__":
    unittest.main()
