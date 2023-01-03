from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json, config

from .open_api_enum_value import OpenAPIEnumValue
from .open_api_property import OpenAPIProperty


@dataclass_json
@dataclass(kw_only=True)
class OpenAPIDefinition:
    format: Optional[str] = field(default=None)
    enum: Optional[list[str]] = field(default=None)
    type: str
    x_enum_values: Optional[list[OpenAPIEnumValue]] = field(default=None, metadata=config(field_name='x-enum-values'))
    properties: Optional[dict[str, OpenAPIProperty]] = field(default=None)

    @property
    def is_enum(self) -> bool:
        if self.x_enum_values:
            return True
        return False
