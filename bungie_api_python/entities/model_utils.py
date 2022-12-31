from datetime import datetime
from typing import TypeVar, Type
from enum import Enum, Flag

from dataclasses_json import config
from marshmallow import fields


EnumType = TypeVar('EnumType', bound=Enum | Flag)


def datetime_field_decoder(st_str: str) -> datetime:
    if st_str:
        return datetime.fromisoformat(st_str.strip('Z').split('.')[0])


def datetime_field_encoder(dt: datetime) -> str:
    if dt:
        return dt.isoformat() + '.00Z'


def int64_enum_encoder(value: EnumType):
    return str(value.value)


def int64_enum_decoder(enum: Type[EnumType]):
    def predicate(value: str) -> EnumType:
        return enum(int(value))

    return predicate


def int64_enum_metadata(enum_type: Type[EnumType]) -> dict[str, dict]:
    return config(
        encoder=int64_enum_encoder,
        decoder=int64_enum_decoder(enum_type),
    )


datetime_metadata = config(
    encoder=datetime_field_encoder,
    decoder=datetime_field_decoder,
    mm_field=fields.DateTime(format='iso')
)
