from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json, config
from marshmallow import fields

from .fields.union import Union
from .header import Header
from .reference import Reference
from .utils import dict_union_dataclass_decoder


@dataclass_json
@dataclass(kw_only=True)
class Encoding:
    contentType: Optional[str] = field(default=None)
    headers: Optional[dict[str, Reference | Header]] = field(
        default=None,
        metadata=config(
            # decoder=dict_union_dataclass_decoder(str, Reference, Header),
            mm_field=fields.Dict(
                keys=fields.String,
                values=Union(fields=[
                    fields.Nested(Reference.schema()),
                    fields.Nested(Header.schema())
                ])
            )
        )
    )
    style: Optional[str] = field(default=None)
    explode: Optional[bool] = field(default=None)
    allowReserved: Optional[bool] = field(default=None)
