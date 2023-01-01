from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .datapoint import Datapoint


@dataclass_json
@dataclass(kw_only=True)
class Series:
    datapoints: list[Datapoint]
    target: str
