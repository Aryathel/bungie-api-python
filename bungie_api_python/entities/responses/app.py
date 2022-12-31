from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .response import Response
from ..applications import Application


@dataclass_json
@dataclass(kw_only=True)
class GetBungieApplications(Response):
    Response: list[Application]
