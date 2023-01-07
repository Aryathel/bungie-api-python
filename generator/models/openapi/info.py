from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json

from .contact import Contact
from .license import License


@dataclass_json
@dataclass(kw_only=True)
class Info:
    title: str
    description: Optional[str] = field(default=None)
    termsOfService: Optional[str] = field(default=None)
    contact: Optional[Contact] = field(default=None)
    license: Optional[License] = field(default=None)
    version: str
