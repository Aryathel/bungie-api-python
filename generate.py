from generator.main import APIGenerator

if __name__ == "__main__":
    gen = APIGenerator()

    gen.gen_readme()
    gen.gen_utils()
    gen.gen_entities()
    gen.write_init()
