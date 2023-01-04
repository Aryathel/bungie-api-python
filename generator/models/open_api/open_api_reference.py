from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass(kw_only=True)
class OpenAPIReference:
    ref: Optional[str] = field(default=None, metadata=config(field_name='$ref'))
