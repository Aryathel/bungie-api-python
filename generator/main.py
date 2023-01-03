import json

import requests

open_api_spec = "https://raw.githubusercontent.com/Bungie-net/api/master/openapi-2.json"


class APIGenerator:
    def __init__(self):
        pass

    @staticmethod
    def get_spec() -> dict:
        with requests.get(open_api_spec) as r:
            r.raise_for_status()
            return r.json()


if __name__ == "__main__":
    data = APIGenerator().get_spec()
    with open('./spec.json', 'w+') as f:
        f.write(json.dumps(data, indent=2))
