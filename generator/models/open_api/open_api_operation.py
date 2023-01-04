from dataclasses import dataclass, field
from typing import Optional, Any

from dataclasses_json import dataclass_json

from .open_api_external_documentation import OpenAPIExternalDocumentation
from .open_api_parameter import OpenAPIParameter
from .open_api_reference import OpenAPIReference
from .open_api_response import OpenAPIResponse


@dataclass_json
@dataclass(kw_only=True)
class OpenAPIOperation:
    tags: Optional[list[str]] = field(default=None)
    summary: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    externalDocs: Optional[OpenAPIExternalDocumentation] = field(default=None)
    operationId: Optional[str] = field(default=None)
    consumes: Optional[list[str]] = field(default=None)
    produces: Optional[list[str]] = field(default=None)
    parameters: Optional[list[OpenAPIParameter | OpenAPIReference]] = field(default=None)
    responses: dict[str, OpenAPIResponse | OpenAPIReference]
    schemes: Optional[list[str]] = field(default=None)
    deprecated: Optional[bool] = field(default=None)
    security: Optional[list[dict[str, list[str]]]] = field(default=None)
