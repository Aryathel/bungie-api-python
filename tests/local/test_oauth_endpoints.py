import unittest
import os

import dotenv

import bungie_api_python
from bungie_api_python.entities.core.enums import OAuthClientType

dotenv.load_dotenv()

api_key = os.getenv("BUNGIE_API_KEY")
client_id = os.getenv("BUNGIE_CLIENT_ID")
if client_id:
    client_id = int(client_id)
client_secret = os.getenv("BUNGIE_CLIENT_SECRET")
client_type = os.getenv("BUNGIE_CLIENT_TYPE")
if client_type:
    client_type = OAuthClientType(int(client_type))
oauth_code = os.getenv("BUNGIE_OAUTH_CODE")

print(f"https://www.bungie.net/en/OAuth/Authorize?client_id={client_id}&response_type=code")


class TestOAuthEndpointsSync(unittest.TestCase):
    def test_get_access_token_sync(self):
        print('RUNNING test_get_access_token_sync TEST')

        client = bungie_api_python.BungieClientSync(
            api_key=api_key,
            client_id=client_id,
            client_secret=client_secret,
            client_type=client_type,
        )

        client.gen_oauth_context(code=oauth_code)

        print(f"SUCCESS: {client._access_token}")


class TestOAuthEndpointsAsync(unittest.IsolatedAsyncioTestCase):
    async def test_get_access_token_async(self):
        print('RUNNING test_get_access_token_async TEST')

        client = bungie_api_python.BungieClientAsync(
            api_key=api_key,
            client_id=client_id,
            client_secret=client_secret,
            client_type=client_type,
        )

        await client.gen_oauth_context(code=oauth_code)

        print(f"SUCCESS: {client._access_token}")


if __name__ == "__main__":
    unittest.main()
