from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json

from .server_variable import ServerVariable


@dataclass_json
@dataclass(kw_only=True)
class Server:
    url: str
    description: Optional[str] = field(default=None)
    variables: Optional[dict[str, ServerVariable]] = field(default=None)
