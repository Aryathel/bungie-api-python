from dataclasses import dataclass, field
from typing import Optional, Any

from dataclasses_json import dataclass_json

from .open_api_header import OpenAPIHeader
from .open_api_schema import OpenAPISchema


@dataclass_json
@dataclass(kw_only=True)
class OpenAPIResponse:
    description: str
    schema: Optional[OpenAPISchema] = field(default=None)
    headers: Optional[dict[str, OpenAPIHeader]] = field(default=None)
    examples: Optional[dict[str, Any]] = field(default=None)
