from dataclasses import dataclass, field
from typing import Optional, Any

from dataclasses_json import dataclass_json

from .server import Server


@dataclass_json
@dataclass(kw_only=True)
class Link:
    operationRef: Optional[str] = field(default=None)
    operationId: Optional[str] = field(default=None)
    parameters: Optional[dict[str, Any]] = field(default=None)
    requestBody: Optional[Any] = field(default=None)
    description: Optional[str] = field(default=None)
    server: Optional[Server] = field(default=None)
