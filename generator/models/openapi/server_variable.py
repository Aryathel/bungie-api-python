from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class ServerVariable:
    enum: Optional[list[str]] = field(default=None)
    default: str
    description: Optional[str] = field(default=None)
