from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class Contact:
    name: Optional[str] = field(default=None)
    url: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)
