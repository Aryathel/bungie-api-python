from dataclasses import dataclass, field
from typing import Optional, Any

from dataclasses_json import dataclass_json

from .open_api_parameter import OpenAPIParameter
from .open_api_reference import OpenAPIReference


@dataclass_json
@dataclass(kw_only=True)
class OpenAPIOperation:
    tags: Optional[list[str]] = field(default=None)
    summary: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    operationId: str = field(default=None)
    parameters: Optional[list[OpenAPIParameter | OpenAPIReference]] = field(default=None)
    requestBody: Optional[Any] = field(default=None)
    responses: dict[str, OpenAPIResponse]
    callbacks: Any = field(default=None)
