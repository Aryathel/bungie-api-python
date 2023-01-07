from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json

from .external_documentation import ExternalDocumentation


@dataclass_json
@dataclass(kw_only=True)
class Tag:
    name: str
    description: Optional[str] = field(default=None)
    externalDocs: Optional[ExternalDocumentation] = field(default=None)
