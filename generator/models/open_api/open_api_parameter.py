from dataclasses import dataclass, field
from typing import Optional, Any

from dataclasses_json import dataclass_json, config

from .open_api_reference import OpenAPIReference
from .open_api_schema import OpenAPISchema


@dataclass_json
@dataclass(kw_only=True)
class OpenAPIParameter:
    name: str
    in_: str = field(metadata=config(field_name='in'))
    description: Optional[str] = field(default=None)
    required: Optional[bool] = field(default=None)
    schema: Optional[OpenAPISchema] = field(default=None)
    type: Optional[str] = field(default=None)
    format: Optional[str] = field(default=None)
    allowEmptyValue: Optional[bool] = field(default=None)
    items: Optional[OpenAPIReference] = field(default=None)
    collectionFormat: Optional[str] = field(default=None)
    default: Optional[Any] = field(default=None)
    maximum: Optional[float] = field(default=None)
    exclusiveMaximum: Optional[bool] = field(default=None)
    minimum: Optional[float] = field(default=None)
    exclusiveMinimum: Optional[bool] = field(default=None)
    maxLength: Optional[int] = field(default=None)
    minLength: Optional[int] = field(default=None)
    pattern: Optional[str] = field(default=None)
    maxItems: Optional[int] = field(default=None)
    minItems: Optional[int] = field(default=None)
    uniqueItems: Optional[bool] = field(default=None)
    enum: Optional[list[Any]] = field(default=None)
    multipleOf: Optional[float] = field(default=None)

