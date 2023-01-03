from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass(kw_only=True)
class OpenAPISecurityDefinition:
    type: str
    description: str
    name: Optional[str] = field(default=None)
    in_: Optional[str] = field(default=None, metadata=config(field_name='in'))
    authorizationUrl: Optional[str] = field(default=None)
    tokenUrl: Optional[str] = field(default=None)
    flow: Optional[str] = field(default=None)
    scopes: dict[str, str]
