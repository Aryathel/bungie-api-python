from dataclasses import dataclass, field
from typing import Iterator

from .enums import ImportType
from ..utils.str_utils import StringUtils


@dataclass
class EntityImport:
    name: str
    type: ImportType
    imports: list[str] = field(default=None)
    self_ref: bool = field(default=False)

    @property
    def specific(self) -> bool:
        return bool(self.imports)

    @property
    def relative(self) -> bool:
        return self.type == ImportType.relative

    @property
    def import_string(self) -> str:
        if self.specific:
            imp = 'from '

            if self.relative:
                imp += f'.{self.name}'
            else:
                imp += self.name

            imp += ' import '
            imp += ', '.join(sorted(self.imports))
        else:
            if self.relative:
                imp = f'import .{self.name}'
            else:
                imp = f'import {self.name}'

        return imp


@dataclass
class EntityImportCollection:
    imports: list[EntityImport] = field(default_factory=list)

    def __iter__(self) -> Iterator[EntityImport]:
        self._i = 0
        return self

    def __next__(self) -> EntityImport:
        if self._i >= len(self.imports):
            raise StopIteration
        val = self.imports[self._i]
        self._i += 1
        return val

    def copy(self) -> 'EntityImportCollection':
        return EntityImportCollection(imports=self.imports.copy())

    def add_import(self, imp: EntityImport) -> None:
        for i in self.imports:
            if i.name == imp.name and i.type == imp.type:
                for i_i in imp.imports:
                    if i_i not in i.imports:
                        i.imports.append(i_i)
                return

        self.imports.append(imp)

    def add_collection(self, imps: 'EntityImportCollection') -> None:
        for imp in imps:
            self.add_import(imp)

    @property
    def imports_sorted(self) -> list[EntityImport]:
        return sorted(self.imports, key=lambda i: i.name.strip('.'))

    @property
    def stdlib_imports(self) -> list[str]:
        return [i.import_string for i in self.imports_sorted if i.type == ImportType.stdlib and not i.self_ref]

    @property
    def external_imports(self) -> list[str]:
        return [i.import_string for i in self.imports_sorted if i.type == ImportType.external and not i.self_ref]

    @property
    def internal_imports(self) -> list[str]:
        return [i.import_string for i in self.imports_sorted if i.type == ImportType.internal and not i.self_ref]

    @property
    def relative_imports(self) -> list[str]:
        return [i.import_string for i in self.imports_sorted if i.type == ImportType.relative and not i.self_ref]

    @property
    def formatted_imports(self) -> str:
        imports = ''

        if self.stdlib_imports:
            imports += StringUtils.gen_line_break_comment('STANDARD LIBRARY IMPORTS')
            imports += '\n'
            imports += '\n'.join(self.stdlib_imports)
            imports += '\n\n'

        if self.external_imports:
            imports += StringUtils.gen_line_break_comment('3RD PARTY LIBRARY IMPORTS')
            imports += '\n'
            imports += '\n'.join(self.external_imports)
            imports += '\n\n'

        if self.internal_imports:
            imports += StringUtils.gen_line_break_comment('LOCAL LIBRARY IMPORTS')
            imports += '\n'
            imports += '\n'.join(self.internal_imports)
            imports += '\n\n'

        if self.relative_imports:
            imports += StringUtils.gen_line_break_comment('INTERNAL LIBRARY IMPORTS')
            imports += '\n'
            imports += '\n'.join(self.relative_imports)
            imports += '\n\n'

        return imports

