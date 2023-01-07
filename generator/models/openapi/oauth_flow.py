from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class OAuthFlow:
    authorizationUrl: str
    tokenUrl: str
    refreshUrl: Optional[str] = field(default=None)
    scopes: dict[str, str]
