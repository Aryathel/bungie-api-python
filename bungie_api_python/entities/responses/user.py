from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .response import Response
from ..config import UserTheme
from ..user.models import GetCredentialTypesForAccountResponse
from ..user import GeneralUser, UserMembershipData, HardLinkedUserMembership


@dataclass_json
@dataclass(kw_only=True)
class GetBungieNetUserById(Response):
    Response: GeneralUser


@dataclass_json
@dataclass(kw_only=True)
class GetSanitizedPlatformDisplayNames(Response):
    Response: dict[str, str]


@dataclass_json
@dataclass(kw_only=True)
class GetCredentialTypesForTargetAccount(Response):
    Response: list[GetCredentialTypesForAccountResponse]


@dataclass_json
@dataclass(kw_only=True)
class GetAvailableThemes(Response):
    Response: list[UserTheme]


@dataclass_json
@dataclass(kw_only=True)
class GetMembershipDataById(Response):
    Response: UserMembershipData


@dataclass_json
@dataclass(kw_only=True)
class GetMembershipDataForCurrentUser(Response):
    Response: UserMembershipData


@dataclass_json
@dataclass(kw_only=True)
class GetMembershipFromHardLinkedCredential(Response):
    Response: HardLinkedUserMembership
