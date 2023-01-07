from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class Discriminator:
    propertyName: str
    mapping: Optional[dict[str, str]] = field(default=None)
