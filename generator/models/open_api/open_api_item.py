from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json, config

from generator.models.open_api.open_api_reference import OpenAPIReference


@dataclass_json
@dataclass(kw_only=True)
class OpenAPIItem:
    format: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)
    ref: Optional[str] = field(default=None, metadata=config(field_name='$ref'))
    x_enum_reference: Optional[OpenAPIReference] = field(default=None, metadata=config(field_name='x-enum-reference'))

    @property
    def is_ref(self) -> bool:
        return self.ref is not None

    @property
    def is_enum(self) -> bool:
        return self.x_enum_reference is not None
