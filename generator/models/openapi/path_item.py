from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json, config
from marshmallow import fields

from .fields.union import Union
from .operation import Operation
from .parameter import Parameter
from .reference import Reference
from .server import Server
from .utils import list_union_dataclass_decoder


@dataclass_json
@dataclass(kw_only=True)
class PathItem:
    ref: Optional[str] = field(default=None, metadata=config(field_name='$ref'))
    summary: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    get: Optional[Operation] = field(default=None)
    put: Optional[Operation] = field(default=None)
    post: Optional[Operation] = field(default=None)
    delete: Optional[Operation] = field(default=None)
    options: Optional[Operation] = field(default=None)
    head: Optional[Operation] = field(default=None)
    patch: Optional[Operation] = field(default=None)
    trace: Optional[Operation] = field(default=None)
    servers: Optional[list[Server]] = field(default=None)
    parameters: Optional[list[Reference | Parameter]] = field(
        default=None,
        metadata=config(
            # decoder=list_union_dataclass_decoder(Reference, Parameter),
            mm_field=fields.List(Union(fields=[
                fields.Nested(Reference.schema()),
                fields.Nested(Parameter.schema()),
            ]))
        )
    )
