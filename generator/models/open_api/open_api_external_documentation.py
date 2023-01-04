from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class OpenAPIExternalDocumentation:
    description: Optional[str] = field(default=None)
    url: str
