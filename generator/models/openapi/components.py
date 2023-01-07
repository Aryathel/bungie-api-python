from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json, config
from marshmallow import fields

from .example import Example
from .fields.union import Union
from .header import Header
from .link import Link
from .parameter import Parameter
from .reference import Reference
from .request_body import RequestBody
from .response import Response
from .schema import Schema
from .security_scheme import SecurityScheme
from .utils import dict_union_dataclass_decoder


@dataclass_json
@dataclass(kw_only=True)
class Components:
    schemas: Optional[dict[str, Reference | Schema]] = field(
        default=None,
        metadata=config(
            # decoder=dict_union_dataclass_decoder(str, Reference, Schema),
            mm_field=fields.Dict(keys=fields.String, values=Union(fields=[
                fields.Nested(Reference.schema()),
                fields.Nested(Schema.schema()),
            ]))
        )
    )
    responses: Optional[dict[str, Reference | Response]] = field(
        default=None,
        metadata=config(
            # decoder=dict_union_dataclass_decoder(str, Reference, Response),
            mm_field=fields.Dict(keys=fields.String, values=Union(fields=[
                fields.Nested(Reference.schema()),
                fields.Nested(Response.schema()),
            ]))
        )
    )
    parameters: Optional[dict[str, Reference | Parameter]] = field(
        default=None,
        metadata=config(
            # decoder=dict_union_dataclass_decoder(str, Reference, Parameter),
            mm_field=fields.Dict(keys=fields.String, values=Union(fields=[
                fields.Nested(Reference.schema()),
                fields.Nested(Parameter.schema()),
            ]))
        )
    )
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
    requestBodies: Optional[dict[str, Reference | RequestBody]] = field(
        default=None,
        metadata=config(
            # decoder=dict_union_dataclass_decoder(str, Reference, RequestBody),
            mm_field=fields.Dict(keys=fields.String, values=Union(fields=[
                fields.Nested(Reference.schema()),
                fields.Nested(RequestBody.schema()),
            ]))
        )
    )
    headers: Optional[dict[str, Reference | Header]] = field(
        default=None,
        metadata=config(
            # decoder=dict_union_dataclass_decoder(str, Reference, Header),
            mm_field=fields.Dict(keys=fields.String, values=Union(fields=[
                fields.Nested(Reference.schema()),
                fields.Nested(Header.schema()),
            ]))
        )
    )
    securitySchemes: Optional[dict[str, Reference | SecurityScheme]] = field(
        default=None,
        metadata=config(
            # decoder=dict_union_dataclass_decoder(str, Reference, SecurityScheme),
            mm_field=fields.Dict(keys=fields.String, values=Union(fields=[
                fields.Nested(Reference.schema()),
                fields.Nested(SecurityScheme.schema()),
            ]))
        )
    )
    links: Optional[dict[str, Reference | Link]] = field(
        default=None,
        metadata=config(
            # decoder=dict_union_dataclass_decoder(str, Reference, Link),
            mm_field=fields.Dict(keys=fields.String, values=Union(fields=[
                fields.Nested(Reference.schema()),
                fields.Nested(Link.schema()),
            ]))
        )
    )
    # callbacks: Optional[dict[str, Reference | Callback]] = field(
    #     default=None,
    #     metadata=config(
    #         decoder=dict_union_dataclass_decoder(str, Reference, Callback)
    #     )
    # )
