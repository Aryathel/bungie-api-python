from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json, config

from .open_api_operation import OpenAPIOperation
from .open_api_parameter import OpenAPIParameter
from .open_api_reference import OpenAPIReference


@dataclass_json
@dataclass(kw_only=True)
class OpenAPIPathItem:
    ref: Optional[str] = field(default=None, metadata=config(field_name='$ref'))
    get: Optional[OpenAPIOperation] = field(default=None)
    put: Optional[OpenAPIOperation] = field(default=None)
    post: Optional[OpenAPIOperation] = field(default=None)
    delete: Optional[OpenAPIOperation] = field(default=None)
    options: Optional[OpenAPIOperation] = field(default=None)
    head: Optional[OpenAPIOperation] = field(default=None)
    patch: Optional[OpenAPIOperation] = field(default=None)
    parameters: list[OpenAPIParameter | OpenAPIReference]
