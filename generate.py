import requests

from generator.main import APIGenerator


def main():
    from generated.entities.responses import IEnumerableOfApplication
    r = requests.get('https://www.bungie.net/Platform/App/FirstParty/', headers={'X-API-Key': 'cfdc38c75e4440f2ae8c581a998ed4d5'})
    r.raise_for_status()
    print(IEnumerableOfApplication.schema().load(r.json()))


if __name__ == "__main__":
    gen = APIGenerator()

    gen.gen_readme()
    gen.gen_utils()
    gen.gen_entities()
    gen.gen_responses()
    gen.write_init()
    main()
