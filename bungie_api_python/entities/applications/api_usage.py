from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .series import Series


@dataclass_json
@dataclass(kw_only=True)
class ApiUsage:
    apiCalls: list[Series]
    throttledRequests: list[Series]
