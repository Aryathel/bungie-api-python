from dataclasses import dataclass, field
from typing import Optional, Any

from dataclasses_json import dataclass_json, config
from marshmallow import fields

from .external_documentation import ExternalDocumentation
from .fields.union import Union
from .parameter import Parameter
from .reference import Reference
from .request_body import RequestBody
from .response import Response
from .server import Server
from .utils import list_union_dataclass_decoder, union_dataclass_decoder, dict_union_dataclass_decoder


@dataclass_json
@dataclass(kw_only=True)
class Operation:
    tags: Optional[list[str]] = field(default=None)
    summary: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    externalDocs: Optional[ExternalDocumentation] = field(default=None)
    operationId: Optional[str] = field(default=None)
    parameters: Optional[list[Reference | Parameter]] = field(
        default=None,
        metadata=config(
            # decoder=list_union_dataclass_decoder(Reference, Parameter),
            mm_field=fields.List(Union(fields=[
                fields.Nested(Reference.schema()),
                fields.Nested(Parameter.schema())
            ]))
        )
    )
    requestBody: Optional[Reference | RequestBody] = field(
        default=None,
        metadata=config(
            # =union_dataclass_decoder(Reference, RequestBody),
            mm_field=Union(fields=[
                fields.Nested(Reference.schema()),
                fields.Nested(RequestBody.schema())
            ])
        )
    )
    responses: dict[str, Reference | Response] = field(
        metadata=config(
            # decoder=dict_union_dataclass_decoder(str, Reference, Response),
            mm_field=fields.Dict(
                keys=fields.String,
                values=Union(fields=[
                    fields.Nested(Reference.schema()),
                    fields.Nested(Response.schema()),
                ])
            )
        )
    )
    # callbacks: Optional[dict[str, Reference | Callback]] = field(
    #     default=None,
    #     metadata=config(
    #         decoder=dict_union_dataclass_decoder(str, Reference, Callback)
    #     )
    # )
    deprecated: Optional[bool] = field(default=None)
    security: Optional[list[dict[str, list[str]]]] = field(default=None)
    servers: Optional[list[Server]] = field(
        default=None,
        metadata=config(mm_field=fields.List(fields.Nested(Server.schema())))
    )

    # Custom
    x_documentation_attributes: Optional[dict[str, Any]] = field(
        default=None,
        metadata=config(field_name='x-documentation-attributes')
    )
    x_preview: Optional[bool] = field(default=None, metadata=config(field_name='x-preview'))
