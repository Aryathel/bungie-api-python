from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json

from ..ignores import IgnoreResponse
from ..model_utils import datetime_metadata


@dataclass_json
@dataclass(kw_only=True)
class UserToUserContext:
    isFollowing: bool
    ignoreStatus: IgnoreResponse
    globalIgnoreEndDate: Optional[datetime] = field(
        default=None,
        metadata=datetime_metadata
    )
