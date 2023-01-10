import os
import unittest

from generator.main import APIGenerator


class Test(unittest.IsolatedAsyncioTestCase):
    async def test_get_bungie_applications(self):
        from generated import BungieClientAsync, BungieClientSync

        client_a = BungieClientAsync(api_key=os.getenv('BUNGIE_API_KEY'))
        apps = await client_a.app.get_bungie_applications()

        client_s = BungieClientSync(api_key=os.getenv('BUNGIE_API_KEY'))
        apps_s = client_s.app.get_bungie_applications()
        assert apps == apps_s


if __name__ == "__main__":
    gen = APIGenerator()

    # Running gen.gen() covers all of these individual calls.
    # gen.gen_readme()
    # gen.gen_utils()
    # gen.gen_entities()
    # gen.gen_responses()
    # gen.gen_endpoints()
    # gen.gen_clients()
    # gen.write_init()

    gen.gen()

    # unittest.main()
