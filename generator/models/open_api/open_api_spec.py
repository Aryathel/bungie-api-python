from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json

from .open_api_definition import OpenAPIDefinition
from .open_api_info import OpenAPIInfo
from .open_api_parameter import OpenAPIParameter
from .open_api_path_item import OpenAPIPathItem
from .open_api_response import OpenAPIResponse
from .open_api_schema import OpenAPISchema
from .open_api_security_definition import OpenAPISecurityScheme
from .open_api_tag import OpenAPITag
from .open_api_external_documentation import OpenAPIExternalDocumentation


@dataclass_json
@dataclass(kw_only=True)
class OpenAPISpec:
    swagger: str
    info: OpenAPIInfo
    host: Optional[str] = field(default=None)
    basePath: Optional[str] = field(default=None)
    schemes: Optional[list[str]] = field(default=None)
    consumes: Optional[list[str]] = field(default=None)
    produces: Optional[list[str]] = field(default=None)
    paths: dict[str, dict[str, OpenAPIPathItem]]
    definitions: Optional[dict[str, OpenAPISchema]] = field(default=None)
    parameters: Optional[dict[str, OpenAPIParameter]] = field(default=None)
    responses: Optional[dict[str, OpenAPIResponse]] = field(default=None)
    securityDefinitions: Optional[dict[str, OpenAPISecurityScheme]] = field(default=None)
    security: Optional[list[dict[str, list[str]]]] = field(default=None)
    tags: Optional[list[OpenAPITag]] = field(default=None)
    externalDocs: Optional[OpenAPIExternalDocumentation] = field(default=None)
