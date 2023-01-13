from dataclasses import dataclass, field
from typing import Optional

from .enums import PropertyType
from ..utils.str_utils import StringUtils


@dataclass
class ClassProperty:
    name: str
    type: str
    optional: bool = field(default=False)
    list: bool = field(default=False)
    dict: bool = field(default=False)
    key_type: str = field(default=None)
    enum: bool = field(default=False)
    byte: bool = field(default=False)
    enum_key: bool = field(default=False)
    forward_ref: bool = field(default=False)
    comment: Optional[str] = field(default=None)
    byte_enum: bool = field(default=False)

    def __post_init__(self) -> None:
        if self.dict and not self.key_type:
            raise KeyError("A property cannot be a dict type without a provided key_type.")

    @property
    def ref_type(self) -> str:
        return f'\'{self.type}\'' if self.forward_ref else self.type

    @property
    def field_type(self) -> str:
        t = ''

        if self.optional:
            t += 'Optional['

        t += self.field_type_required

        if self.optional:
            t += ']'

        return t

    @property
    def field_type_required(self) -> str:
        t = ''
        if self.dict:
            t += f'dict[{PropertyType(self.key_type).python_type if not self.enum_key else self.key_type}, '
        if self.list:
            t += f'list['

        t += self.ref_type

        if self.list:
            t += ']'
        if self.dict:
            t += ']'

        return t

    @property
    def forward_ref_mm_field(self) -> str:
        arg = 'mm_field='

        if self.dict:
            arg += f'{PropertyType.object.mm_type}(keys={PropertyType(self.key_type).mm_type if not self.enum_key else "fields.Enum(" + self.key_type+ ", by_value=" + str(not self.byte_enum) + ")"}, values='
        if self.list:
            arg += PropertyType.array.mm_type + '('

        if self.forward_ref:
            arg += f'fields.Nested(lambda: {self.type}.schema())'
        elif self.enum and self.byte_enum:
            arg += f'fields.Enum({self.type}, by_value=False)'
        else:
            arg += PropertyType.from_python_type(self.type).mm_type

        if self.list:
            arg += ')'
        if self.dict:
            arg += ')'

        return arg

    @property
    def field_value(self) -> str:
        val = ''

        args = []

        if self.optional:
            args.append('default=None')
        if self.type == 'datetime':
            args.append('metadata=config(mm_field=fields.DateTime(format=\'iso\'))')
        if self.byte:
            args.append('metadata=config(mm_field=UnionField(fields=[fields.Integer, fields.String]))')
        if self.forward_ref:
            args.append(f'metadata=config({self.forward_ref_mm_field})')
        elif self.byte_enum:
            args.append(f'metadata=config({self.forward_ref_mm_field})')

        if args:
            val += f' = field('
            val += ', '.join(args)
            val += ')'

        return val

    @property
    def field_definition(self) -> str:
        if not self.comment:
            return f'{StringUtils.indent}{self.name}: {self.field_type}{self.field_value}'
        else:
            return f'{StringUtils.gen_comment(self.comment, depth=1)}\n' \
                   f'{StringUtils.indent}{self.name}: {self.field_type}{self.field_value}'
