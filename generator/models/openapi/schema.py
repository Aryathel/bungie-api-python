from dataclasses import dataclass, field
from typing import Optional, Any

import typing
from dataclasses_json import dataclass_json, config
from marshmallow import fields

from .custom.enum_value import EnumValue
from .discriminator import Discriminator
from .external_documentation import ExternalDocumentation
from .fields.union import Union
from .reference import Reference
from .xml import XML


@dataclass_json
@dataclass(kw_only=True)
class Schema:
    # Any instance validation
    type: Optional[str] = field(default=None)
    enum: Optional[list[Any]] = field(default=None)

    # Numeric validation
    multipleOf: Optional[float] = field(default=None)
    maximum: Optional[float] = field(default=None)
    exclusiveMaximum: Optional[float] = field(default=None)
    minimum: Optional[float] = field(default=None)
    exclusiveMinimum: Optional[float] = field(default=None)

    # String validation
    maxLength: Optional[int] = field(default=None)
    minLength: Optional[int] = field(default=None)
    pattern: Optional[str] = field(default=None)

    # Array validation
    maxItems: Optional[int] = field(default=None)
    minItems: Optional[int] = field(default=None)
    uniqueItems: Optional[bool] = field(default=None)

    # Object validation
    maxProperties: Optional[int] = field(default=None)
    minProperties: Optional[int] = field(default=None)
    required: Optional[list[str]] = field(default=None)

    # Metadata annotations
    title: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    default: Optional[Any] = field(default=None)

    # Core schema elements
    allOf: Optional[list['Schema']] = field(
        default=None,
        metadata=config(
            mm_field=fields.List(fields.Nested(lambda: Schema.schema()))
        )
    )
    oneOf: Optional[list['Schema']] = field(
        default=None,
        metadata=config(
            mm_field=fields.List(fields.Nested(lambda: Schema.schema()))
        )
    )
    anyOf: Optional[list['Schema']] = field(
        default=None,
        metadata=config(
            mm_field=fields.List(fields.Nested(lambda: Schema.schema()))
        )
    )
    not_: Optional['Schema'] = field(
        default=None,
        metadata=config(
            field_name='not',
            mm_field=fields.Nested(lambda: Schema.schema())
        )
    )
    items: Optional['Schema'] = field(
        default=None,
        metadata=config(
            mm_field=fields.Nested(lambda: Schema.schema())
        )
    )
    properties: Optional[dict[str, 'Schema']] = field(
        default=None,
        metadata=config(
            mm_field=fields.Dict(
                keys=fields.String,
                values=fields.Nested(lambda: Schema.schema())
            )
        )
    )
    additionalProperties: Optional[typing.Union[Reference,  'Schema']] = field(
        default=None,
        metadata=config(
            mm_field=Union(fields=[
                fields.Nested(Reference.schema()),
                fields.Nested(lambda: Schema.schema()),
            ])
        )
    )

    # Output
    format: Optional[str] = field(default=None)

    # Other
    nullable: Optional[bool] = field(default=None)
    discriminator: Optional[Discriminator] = field(default=None)
    readOnly: Optional[bool] = field(default=None)
    writeOnly: Optional[bool] = field(default=None)
    xml: Optional[XML] = field(default=None)
    externalDocs: Optional[ExternalDocumentation] = field(default=None)
    example: Optional[Any] = field(default=None)
    deprecated: Optional[bool] = field(default=None)

    # Custom fields:
    ref: Optional[str] = field(default=None, metadata=config(field_name='$ref'))
    x_dictionary_key: Optional['Schema'] = field(
        default=None,
        metadata=config(
            field_name='x-dictionary-key',
            mm_field=fields.Nested(lambda: Schema.schema(), data_key='x-dictionary-key')
        )
    )
    x_enum_reference: Optional[Reference] = field(default=None, metadata=config(field_name='x-enum-reference'))
    x_enum_is_bitmask: Optional[bool] = field(default=None, metadata=config(field_name='x-enum-is-bitmask'))
    x_enum_values: Optional[list[EnumValue]] = field(default=None, metadata=config(field_name='x-enum-values'))
    x_preview: Optional[bool] = field(default=None, metadata=config(field_name='x-preview'))
    x_mapped_definition: Optional[Reference] = field(default=None, metadata=config(field_name='x-mapped-definition'))
    x_mobile_manifest_name: Optional[str] = field(default=None, metadata=config(field_name='x-mobile-manifest-name'))
    x_destiny_component_type_dependency: Optional[str] = field(
        default=None,
        metadata=config(field_name='x-destiny-component-type-dependency')
    )
