from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json, config

from .open_api_reference import OpenAPIReference


@dataclass_json
@dataclass(kw_only=True)
class OpenAPIProperty:
    format: Optional[str] = field(default=None)
    description: str
    type: str
    x_enum_reference: Optional[OpenAPIReference] = field(default=None, metadata=config(field_name='x-enum-reference'))
    items: Optional['OpenAPIProperty'] = field(default=None)
