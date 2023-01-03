from dataclasses import dataclass

from dataclasses_json import dataclass_json


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
