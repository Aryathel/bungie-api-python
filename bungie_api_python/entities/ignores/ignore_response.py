from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .enums import IgnoreStatus


@dataclass_json
@dataclass(kw_only=True)
class IgnoreResponse:
    isIgnored: bool
    ignoreFlags: IgnoreStatus
