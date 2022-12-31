from dataclasses import dataclass

from dataclasses_json import dataclass_json

from . import DeveloperRole
from ..user import UserInfoCard


@dataclass_json
@dataclass(kw_only=True)
class ApplicationDeveloper:
    role: DeveloperRole
    apiEulaVersion: int
    user: UserInfoCard
