from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .open_api_parameter import OpenAPIParameter
from .open_api_response import OpenAPIResponse


@dataclass_json
@dataclass(kw_only=True)
class OpenAPIPath:
    tags: list[str]
    description: str
    operationId: str
    parameters: list[OpenAPIParameter]
    deprecated: bool
    security: list[dict[str, list[str]]]
    responses: dict[str, OpenAPIResponse]
