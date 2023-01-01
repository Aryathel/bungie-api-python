from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .response import Response
from ..user.general_user import GeneralUser


@dataclass_json
@dataclass(kw_only=True)
class GetBungieNetUserById(Response):
    Response: GeneralUser
