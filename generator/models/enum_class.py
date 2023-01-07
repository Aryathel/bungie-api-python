from .entity_import import EntityImportCollection, EntityImport
from .enums import ImportType
from .openapi.custom.enum_value import EnumValue as EnumVal
from .openapi.schema import Schema
from ..utils.str_utils import StringUtils


class EnumValue:
    value: str | int

    def __init__(self, enm: EnumVal, t: str, fmt: str) -> None:
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
    enum_path_name = 'enums'

    values: list[EnumValue]
    imp: EntityImport

    def __init__(self, qualified_name: str, entity: Schema) -> None:
        self.name = qualified_name.split('.')[-1]
        self.qualified_name = qualified_name
        self.entity = entity

        self.values = []
        for val in entity.x_enum_values:
            self.add_value(val)
        self.imp = EntityImport(
            name='enum',
            type=ImportType.stdlib,
            imports=[self.type]
        )

    def add_value(self, val: EnumVal) -> None:
        self.values.append(EnumValue(val, self.entity.type, self.entity.format))

    @property
    def init_import(self) -> str:
        return EntityImport(
            name=self.enum_path_name,
            type=ImportType.relative,
            imports=[self.name_safe]
        ).import_string

    @property
    def name_safe(self) -> str:
        return self.name.replace('[]', 'Array')

    @property
    def values_sorted(self) -> list[EnumValue]:
        return sorted(self.values, key=lambda v: v.value)

    @property
    def is_flag(self) -> bool:
        return self.entity.x_enum_is_bitmask

    @property
    def type(self) -> str:
        return 'Flag' if self.is_flag else 'Enum'

    @property
    def formatted_enum(self) -> str:
        content = StringUtils.gen_line_break_comment(self.qualified_name)
        content += '\n'
        content += StringUtils.gen_class_declaration(self.name, inheritance=[self.type])
        content += '\n'
        content += '\n'.join([i.formatted_value for i in self.values_sorted])

        return content


class EnumCollection:
    enums: list[EnumClass]
    imports: EntityImportCollection

    def __init__(self):
        self.enums = []
        self.imports = EntityImportCollection()

    @property
    def enum_models_text_content(self) -> str:
        content = self.imports.formatted_imports
        content += '\n'
        content += '\n\n\n'.join(e.formatted_enum for e in self.enums)
        content += '\n'
        return content

    @property
    def enum_names(self) -> list[str]:
        return [e.name_safe for e in self.enums]

    @property
    def init_imports(self) -> list[str]:
        return [e.init_import for e in self.enums]

    def add_enum(self, name: str, schema: Schema) -> None:
        enm = EnumClass(name, schema)
        self.enums.append(enm)
        self.imports.add_import(enm.imp)

    def write_enum_file(self, file: str) -> None:
        with open(file, 'w+') as enum_file:
            enum_file.write(self.enum_models_text_content)
