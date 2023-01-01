from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json

from ...core import BungieCredentialType


@dataclass_json
@dataclass(kw_only=True)
class GetCredentialTypesForAccountResponse:
    credentialType: BungieCredentialType
    credentialDisplayName: str
    isPublic: bool
    credentialAsString: Optional[str] = field(default=None)
