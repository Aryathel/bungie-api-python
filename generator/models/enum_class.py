from .open_api.open_api_enum_value import OpenAPIEnumValue
from ..utils.str_utils import StringUtils


class EnumValue:
    value: str | int

    def __init__(self, enm: OpenAPIEnumValue, t: str, fmt: str) -> None:
        self.name = enm.identifier
        self._val = enm.numericValue
        self.type = t
        self.format = fmt
        self.desc = enm.description

        self.process_value()

    def __repr__(self) -> str:
        return f'<{self.name}: {self.val_repr}>'

    def __str__(self) -> str:
        return self.__repr__()

    def process_value(self) -> None:
        if self.type == 'integer':
            self.value = int(self._val)
        elif self.type == 'string':
            self.value = str(self._val)

    @property
    def name_safe(self) -> str:
        if self.name == 'None':
            return 'None_'
        return self.name

    @property
    def val_repr(self) -> str:
        if self.type == 'integer':
            return str(self.value)
        elif self.type == 'string':
            return f'\'{self.value}\''

    @property
    def formatted_value(self) -> str:
        val = f'{self.name_safe} = {self.val_repr}'

        if self.desc:
            return f'{StringUtils.gen_comment(self.desc, 1)}\n{StringUtils.indent_str(val, 1)}'
        else:
            return StringUtils.indent_str(val, 1)


class EnumClass:
    values: list[EnumValue]

    def __init__(self, name: str, t: str, fmt: str) -> None:
        self.name = name
        self.t = t
        self.fmt = fmt

        self.values = []

    def add_value(self, val: OpenAPIEnumValue) -> None:
        self.values.append(EnumValue(val, self.t, self.fmt))

    @property
    def values_sorted(self) -> list[EnumValue]:
        return sorted(self.values, key=lambda v: v.value)

    @property
    def is_flag(self) -> bool:
        if self.t == 'string':
            return False

        vals = self.values_sorted

        if (len(vals) > 2 and vals[-1].value > 3) or 'flag' in self.name.lower():
            return vals[-1].value / 2 == vals[-2].value

        return False

    @property
    def _is_int_enum_def(self) -> str:
        content = StringUtils.indent_str('@property\n', 1)
        content += StringUtils.indent_str('def _is_int_enum(self) -> bool:\n', 1)
        if self.t == 'integer':
            content += StringUtils.indent_str('return True', 2)
        else:
            content += StringUtils.indent_str('return False', 2)

        return content

    @property
    def formatted_enum(self) -> str:
        type = 'Flag' if self.is_flag else 'Enum'

        content = StringUtils.gen_line_break_comment('STANDARD LIBRARY IMPORTS')
        content += '\n'
        content += StringUtils.gen_import('enum', [type])
        content += '\n\n\n'

        content += StringUtils.gen_line_break_comment('ENUM DEFINITION')
        content += '\n'

        content += f'class {self.name}({type}):\n'
        content += '\n'.join([i.formatted_value for i in self.values_sorted])
        content += '\n\n'
        content += self._is_int_enum_def
        content += '\n'

        return content
