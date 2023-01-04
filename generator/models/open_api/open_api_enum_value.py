from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class OpenAPIEnumValue:
    numericValue: int
    identifier: str
    description: Optional[str] = field(default=None)
