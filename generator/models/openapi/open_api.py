from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json

from .components import Components
from .external_documentation import ExternalDocumentation
from .info import Info
from .path_item import PathItem
from .server import Server
from .tag import Tag


@dataclass_json
@dataclass(kw_only=True)
class OpenApi:
    openapi: str
    info: Info
    servers: Optional[list[Server]] = field(default=None)
    paths: dict[str, PathItem]
    components: Optional[Components] = field(default=None)
    security: Optional[list[dict[str, list[str]]]] = field(default=None)
    tags: Optional[list[Tag]] = field(default=None)
    externalDocs: Optional[ExternalDocumentation] = field(default=None)
