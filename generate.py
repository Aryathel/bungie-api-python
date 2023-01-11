from generator.main import APIGenerator


if __name__ == "__main__":
    gen = APIGenerator()

    # Running gen.gen() covers all of these individual calls.
    # self.gen_entities()
    # self.gen_readme()
    # self.gen_utils()
    # self.gen_responses()
    # self.gen_endpoints()
    # self.gen_security()
    # self.gen_clients()
    #self.write_init()

    gen.gen()
