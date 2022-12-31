from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json, config

from . import ApplicationScopes, ApplicationStatus, ApplicationDeveloper
from ..model_utils import datetime_metadata, int64_enum_metadata


@dataclass_json
@dataclass(kw_only=True)
class Application:
    applicationId: int
    name: str
    redirectUrl: str
    link: str
    scope: ApplicationScopes = field(metadata=int64_enum_metadata(ApplicationScopes))
    origin: Optional[str] = field(default=None)
    status: ApplicationStatus
    creationDate: datetime = field(metadata=datetime_metadata)
    firstPublished: datetime = field(metadata=datetime_metadata)
    team: list[ApplicationDeveloper]
    overrideAuthorizeViewName: Optional[str] = field(default=None)
