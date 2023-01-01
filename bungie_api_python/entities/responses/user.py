from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .response import Response
from ..user.general_user import GeneralUser
from ..user.models.get_credential_types_for_account_response import GetCredentialTypesForAccountResponse


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
