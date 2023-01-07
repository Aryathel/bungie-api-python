from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json

from .media_type import MediaType


@dataclass_json
@dataclass(kw_only=True)
class RequestBody:
    description: Optional[str] = field(default=None)
    content: dict[str, MediaType]
    required: Optional[bool] = field(default=None)
