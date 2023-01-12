from generator.main import APIGenerator


if __name__ == "__main__":
    gen = APIGenerator()

    # Running gen.gen() covers all of these individual calls.
    # gen.gen_entities()
    # gen.gen_readme()
    # gen.gen_utils()
    # gen.gen_responses()
    # gen.gen_endpoints()
    # gen.gen_security()
    # gen.gen_clients()
    # gen.write_init()

    gen.gen()
