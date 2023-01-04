from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .open_api_contact import OpenAPIContact
from .open_api_license import OpenAPILicense


@dataclass_json
@dataclass(kw_only=True)
class OpenAPIInfo:
    title: str
    description: str
    termsOfService: str
    contact: OpenAPIContact
    license: OpenAPILicense
    version: str
