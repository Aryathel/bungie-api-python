from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json

from .oauth_flow import OAuthFlow


@dataclass_json
@dataclass(kw_only=True)
class OAuthFlows:
    implicit: Optional[OAuthFlow] = field(default=None)
    password: Optional[OAuthFlow] = field(default=None)
    clientCredentials: Optional[OAuthFlow] = field(default=None)
    authorizationCode: Optional[OAuthFlow] = field(default=None)
