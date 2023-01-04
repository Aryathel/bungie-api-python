from dataclasses import dataclass, field
from typing import Optional, Any, Union

from dataclasses_json import dataclass_json, config

from .open_api_enum_value import OpenAPIEnumValue
from .open_api_item import OpenAPIItem
from .open_api_reference import OpenAPIReference


@dataclass_json
@dataclass(kw_only=True)
class OpenAPIProperty:
    ref: Optional[str] = field(default=None, metadata=config(field_name='$ref'))
    format: Optional[str] = field(default=None)
    title: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    default: Optional[Any] = field(default=None)
    enum: Optional[list[Any]] = field(default=None)
    x_enum_values: Optional[list[OpenAPIEnumValue]] = field(default=None, metadata=config(field_name='x-enum-values'))
    items: Optional[OpenAPIItem] = field(default=None)
    x_enum_reference: Optional[OpenAPIReference] = field(default=None, metadata=config(field_name='x-enum-reference'))

    @property
    def is_ref(self) -> bool:
        return self.ref is not None

    @property
    def is_enum_property(self) -> bool:
        return self.x_enum_reference is not None
