from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class License:
    name: str
    url: Optional[str] = field(default=None)
