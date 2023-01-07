from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class XML:
    name: Optional[str] = field(default=None)
    namespace: Optional[str] = field(default=None)
    prefix: Optional[str] = field(default=None)
    attribute: Optional[bool] = field(default=None)
    wrapper: Optional[bool] = field(default=None)
