from dataclasses import dataclass, field
from typing import Any, Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class Example:
    summary: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    value: Optional[Any] = field(default=None)
    externalValue: Optional[str] = field(default=None)
