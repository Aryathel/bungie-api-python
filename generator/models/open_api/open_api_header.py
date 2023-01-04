from dataclasses import dataclass, field
from typing import Optional, Any

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class OpenAPIHeader:
    description: Optional[str] = field(default=None)
    type: str
    format: Optional[str] = field(default=None)
    items: Optional[Any] = field(default=None)
    collectionFormat: Optional[str] = field(default=None)
    default: Optional[Any] = field(default=None)
    maximum: Optional[float] = field(default=None)
    exclusiveMaximum: Optional[bool] = field(default=None)
    minimum: Optional[float] = field(default=None)
    exclusiveMinimum: Optional[bool] = field(default=None)
    maxLength: Optional[int] = field(default=None)
    minLength: Optional[int] = field(default=None)
    pattern: Optional[str] = field(default=None)
    maxItems: Optional[int] = field(default=None)
    minItems: Optional[int] = field(default=None)
    uniqueItems: Optional[bool] = field(default=None)
    enum: Optional[list[Any]] = field(default=None)
    multipleOf: Optional[float] = field(default=None)
