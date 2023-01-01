from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json

from .user_info_card import UserInfoCard


@dataclass_json
@dataclass(kw_only=True)
class UserSearchResponseDetail:
    bungieGlobalDisplayName: Optional[str] = field(default=None)
    bungieGlobalDisplayNameCode: Optional[int] = field(default=None)
    bungieNetMembershipId: Optional[int] = field(default=None)
    destinyMemberships: list[UserInfoCard]
