from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json

from ..groupsv2 import GroupUserInfoCard
from .general_user import GeneralUser


@dataclass_json
@dataclass(kw_only=True)
class UserMembershipData:
    destinyMemberships: list[GroupUserInfoCard]
    primaryMembershipId: Optional[int] = field(default=None)
    bungieNetUser: GeneralUser
