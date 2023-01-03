from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass(kw_only=True)
class OpenAPIReference:
    ref: str = field(metadata=config(field_name='$ref'))
