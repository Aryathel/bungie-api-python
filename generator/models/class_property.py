from dataclasses import dataclass, field
from typing import Optional

from ..utils.str_utils import StringUtils


@dataclass
class ClassProperty:
    name: str
    type: str
    optional: bool = field(default=False)
    list: bool = field(default=False)
    is_enum: bool = field(default=False)
    comment: Optional[str] = field(default=None)

    @property
    def field_type(self) -> str:
        t = ''

        if self.optional:
            t += 'Optional['

        if self.list:
            t += f'list[{self.type}]'
        else:
            t += self.type

        if self.optional:
            t += ']'

        return t

    @property
    def field_value(self) -> str:
        val = ''

        args = []

        if self.optional:
            args.append('default=None')
        if self.type == 'datetime':
            args.append('metadata=DATETIME_META')
        if self.is_enum:
            args.append('metadata=ENUM_META')

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
