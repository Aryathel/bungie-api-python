from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json

from bungie_api_python.entities.core import BungieMembershipType


@dataclass_json
@dataclass(kw_only=True)
class HardLinkedUserMembership:
    membershipType: BungieMembershipType
    membershipId: int
    CrossSaveOverriddenType: BungieMembershipType
    CrossSaveOverridenMembershipId: Optional[int] = field(default=None)
