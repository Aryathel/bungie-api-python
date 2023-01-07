from dataclasses import dataclass, field
from typing import Optional, Any

from dataclasses_json import dataclass_json, config
from marshmallow import fields

from .example import Example
from .fields.union import Union
from .reference import Reference
from .schema import Schema
from .utils import union_dataclass_decoder, dict_union_dataclass_decoder


@dataclass_json
@dataclass(kw_only=True)
class Header:
    description: Optional[str] = field(default=None)
    required: Optional[bool] = field(default=None)
    deprecated: Optional[bool] = field(default=None)
    allowEmptyValue: Optional[bool] = field(default=None)

    style: Optional[str] = field(default=None)
    explode: Optional[bool] = field(default=None)
    allowReserved: Optional[bool] = field(default=None)
    schema: Optional[Reference | Schema] = field(
        default=None,
        metadata=config(
            # decoder=union_dataclass_decoder(Reference, Schema),
            mm_field=Union(fields=[fields.Nested(Reference.schema()), fields.Nested(Schema.schema())])
        )
    )
    example: Optional[Any] = field(default=None)
    examples: Optional[dict[str, Reference | Example]] = field(
        default=None,
        metadata=config(
            # decoder=dict_union_dataclass_decoder(str, Reference, Example),
            mm_field=fields.Dict(keys=fields.String, values=Union(fields=[
                fields.Nested(Reference.schema()),
                fields.Nested(Example.schema()),
            ]))
        )
    )

    # content: Optional[dict[str, MediaType]] = field(default=None)
