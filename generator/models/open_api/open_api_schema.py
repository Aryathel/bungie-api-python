from dataclasses import dataclass, field
from typing import Optional, Any

from dataclasses_json import dataclass_json, config

from .open_api_enum_value import OpenAPIEnumValue
from .open_api_property import OpenAPIProperty
from .open_api_reference import OpenAPIReference
from .open_api_external_documentation import OpenAPIExternalDocumentation


@dataclass_json
@dataclass(kw_only=True)
class OpenAPISchema:
    ref: Optional[str] = field(default=None, metadata=config(field_name='$ref'))
    format: Optional[str] = field(default=None)
    title: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
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
    x_enum_values: Optional[list[OpenAPIEnumValue]] = field(default=None, metadata=config(field_name='x-enum-values'))
    multipleOf: Optional[float] = field(default=None)

    items: Optional[OpenAPIReference] = field(default=None)
    allOf: Optional[list[OpenAPIReference]] = field(default=None)
    properties: Optional[dict[str, OpenAPIProperty]] = field(default=None)

    discriminator: Optional[str] = field(default=None)
    readOnly: Optional[bool] = field(default=None)
    xml: Optional[Any] = field(default=None)
    externalDocs: Optional[OpenAPIExternalDocumentation] = field(default=None)
    example: Optional[Any] = field(default=None)

    @property
    def is_enum(self) -> bool:
        return self.x_enum_values is not None
