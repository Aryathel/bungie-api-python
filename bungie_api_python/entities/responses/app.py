from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .response import Response
from ..applications import Application, ApiUsage


@dataclass_json
@dataclass(kw_only=True)
class GetApplicationApiUsage(Response):
    Response: ApiUsage


@dataclass_json
@dataclass(kw_only=True)
class GetBungieApplications(Response):
    Response: list[Application]
