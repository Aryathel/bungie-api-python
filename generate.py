from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json

from generator.main import APIGenerator


@dataclass_json
@dataclass
class TestDT1:
    value: Optional['TestDT2'] = field(default=None)


@dataclass_json
@dataclass
class TestDT2:
    value: Optional[TestDT1] = field(default=None)
    item: Optional[str] = field(default=None)


def test():
    from generated import entities

    print(entities.__all__)


if __name__ == "__main__":
    #gen = APIGenerator()

    #gen.gen_utils()
    #gen.gen_entities()
    #gen.gen_readme()

    test()
