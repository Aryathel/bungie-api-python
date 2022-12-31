import abc
from dataclasses import dataclass, field
from typing import Any, Optional

from dataclasses_json import dataclass_json

from ..exceptions import PlatformErrorCodes


@dataclass_json
@dataclass(kw_only=True)
class Response(abc.ABC):
    Response: Any
    ErrorCode: PlatformErrorCodes
    ThrottleSeconds: int
    ErrorStatus: str
    Message: str
    MessageData: dict[str, str]
    DetailedErrorTrace: Optional[str] = field(default=None)
