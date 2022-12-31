from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json

from ..core import BungieMembershipType


@dataclass_json
@dataclass(kw_only=True)
class UserInfoCard:
    supplementalDisplayName: str
    iconPath: str
    crossSaveOverride: BungieMembershipType
    applicableMembershipTypes: Optional[list[BungieMembershipType]] = field(default=None)
    isPublic: bool
    membershipType: BungieMembershipType
    membershipId: int
    displayName: str
    bungieGlobalDisplayName: Optional[str] = field(default=None)
    bungieGlobalDisplayNameCode: Optional[int] = field(default=None)
