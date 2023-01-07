from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json, config

from .oauth_flows import OAuthFlows


@dataclass_json
@dataclass(kw_only=True)
class SecurityScheme:
    type: str
    description: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    in_: Optional[str] = field(default=None, metadata=config(field_name='in'))
    scheme: Optional[str] = field(default=None)
    bearerFormat: Optional[str] = field(default=None)
    flows: Optional[OAuthFlows] = field(default=None)
    openIdConnectUrl: Optional[str] = field(default=None)
