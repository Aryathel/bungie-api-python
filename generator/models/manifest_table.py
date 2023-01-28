import os
from typing import Iterator

from .entity import Entity
from .entity_import import EntityImportCollection, EntityImport
from .enums import ImportType
from ..utils.str_utils import StringUtils


class ManifestTable:
    entities_path_name = 'entities'
    utils_path_name = 'utils'
    exceptions_path_name = 'exceptions'
    manifest_client_name = 'manifest_client'
    manifest_tables_path = 'manifest_tables'
    file_extension = '.py'

    def __init__(self, entity: Entity) -> None:
        if not entity.is_manifest_definition:
            raise ValueError("The provided entity must be a manifest definition entity.")

        self.entity = entity
        self.default_imports = EntityImportCollection([
            EntityImport(
                name=f'.{self.entities_path_name}',
                type=ImportType.relative,
                imports=[self.table_name]
            ),
            EntityImport(
                name='marshmallow',
                type=ImportType.external,
                imports=['ValidationError'],
            ),
            EntityImport(
                name=f'.{self.utils_path_name}.{self.exceptions_path_name}',
                type=ImportType.relative,
                imports=['ManifestValidationError'],
            ),
        ])

    @property
    def init_imports(self) -> EntityImportCollection:
        return EntityImportCollection([
            EntityImport(
                name=self.manifest_tables_path + '_sync',
                type=ImportType.relative,
                imports=[self.sync_name],
            ),
            EntityImport(
                name=self.manifest_tables_path + '_async',
                type=ImportType.relative,
                imports=[self.async_name],
            ),
        ])

    @property
    def async_imports(self) -> EntityImportCollection:
        imp = self.default_imports.copy()
        imp.add_import(EntityImport(
            name=f'.{self.manifest_client_name}_async',
            type=ImportType.relative,
            imports=['ManifestClientAsync'],
            type_check=True,
        ))
        return imp

    @property
    def sync_imports(self) -> EntityImportCollection:
        imp = self.default_imports.copy()
        imp.add_import(EntityImport(
            name=f'.{self.manifest_client_name}_sync',
            type=ImportType.relative,
            imports=['ManifestClientSync'],
            type_check=True,
        ))
        return imp

    @property
    def name(self) -> str:
        return self.entity.manifest_name

    @property
    def async_name(self) -> str:
        return f'{self.name}Async'

    @property
    def sync_name(self) -> str:
        return f'{self.name}Sync'

    @property
    def table_name(self) -> str:
        return self.entity.name

    @property
    def file_name(self) -> str:
        return StringUtils.camel_to_snake(self.name)

    @staticmethod
    def init_method(is_async: bool) -> list[str]:
        items = [
            StringUtils.gen_function_declaration(
                func_name='__init__',
                params=['self', f'parent: \'ManifestClient{"Async" if is_async else "Sync"}\''],
                response_type='None',
            ),
            StringUtils.indent_str('self.manifest_client = parent', 1),
        ]
        return items

    def validate_method(self, is_async: bool) -> list[str]:
        return [
            StringUtils.gen_function_declaration(
                func_name='validate',
                params=['self'],
                response_type='bool',
                is_async=is_async,
            ),
            StringUtils.indent_str(
                f'res = {"await " if is_async else ""}self.manifest_client.query_mobile_content(',
                1,
            ),
            StringUtils.indent_str('query=f\'\'\'SELECT * FROM {self.table_name};\'\'\',', 2),
            StringUtils.indent_str('many=True,', 2),
            StringUtils.indent_str(')', 1),
            StringUtils.indent_str('errors = ManifestValidationError()', 1),
            StringUtils.indent_str('for r in res:', 1),
            StringUtils.indent_str('try:', 2),
            StringUtils.indent_str(f'{self.table_name}.schema().loads(r[\'json\'])', 3),
            StringUtils.indent_str('except ValidationError as e:', 2),
            StringUtils.indent_str('for f, es in e.messages_dict.items():', 3),
            StringUtils.indent_str('errors.add_error(f, es)', 4),
            StringUtils.indent_str('errors.raise_exception()', 1),
            StringUtils.indent_str('return True', 1),
        ]

    @staticmethod
    def count_method(is_async: bool) -> list[str]:
        return [
            StringUtils.gen_function_declaration(
                func_name='count',
                params=['self'],
                response_type='int',
                is_async=is_async,
            ),
            StringUtils.indent_str(
                f'res = {"await " if is_async else ""}self.manifest_client.query_mobile_content(',
                1,
            ),
            StringUtils.indent_str('query=f\'\'\'SELECT COUNT(*) AS [count] FROM {self.table_name};\'\'\',', 2),
            StringUtils.indent_str('many=False,', 2),
            StringUtils.indent_str(')', 1),
            StringUtils.indent_str('return res[\'count\']', 1),
        ]

    def get_all_method(self, is_async: bool) -> list[str]:
        return [
            StringUtils.gen_function_declaration(
                func_name='get_all',
                params=['self'],
                response_type=f'list[{self.table_name}]',
                is_async=is_async,
            ),
            StringUtils.indent_str(
                f'res = {"await " if is_async else ""}self.manifest_client.query_mobile_content(',
                1,
            ),
            StringUtils.indent_str(f'query=f\'\'\'SELECT * FROM {{self.table_name}};\'\'\',', 2),
            StringUtils.indent_str('many=True,', 2),
            StringUtils.indent_str(')', 1),
            StringUtils.indent_str(f'return [{self.table_name}.schema().loads(r[\'json\']) for r in res]', 1),
        ]

    def text_content(self, is_async: bool) -> str:
        content = StringUtils.gen_class_declaration(class_name=self.async_name if is_async else self.sync_name)
        content += '\n'
        content += StringUtils.indent_str(f'table_name = \'{self.table_name}\'', 1)
        content += '\n\n'

        content += '\n'.join(StringUtils.indent_str(l, 1) for l in self.init_method(is_async))
        content += '\n\n'

        content += '\n'.join(StringUtils.indent_str(l, 1) for l in self.validate_method(is_async))
        content += '\n\n'

        content += '\n'.join(StringUtils.indent_str(l, 1) for l in self.count_method(is_async))
        content += '\n\n'

        content += '\n'.join(StringUtils.indent_str(l, 1) for l in self.get_all_method(is_async))
        content += '\n'

        return content


class ManifestClient:
    manifest_tables_path = 'manifest_tables'
    client_file_path = 'manifest_client'
    manifest_class_name = 'ManifestClient'
    file_extension = '.py'

    tables: list[ManifestTable]

    def __init__(self) -> None:
        self.tables = []

    def __iter__(self) -> Iterator[ManifestTable]:
        for t in self.tables:
            yield t

    def add_manifest_table(self, entity: Entity) -> None:
        self.tables.append(ManifestTable(entity))

    def tables_text_content(self, is_async: bool) -> str:
        imports = EntityImportCollection()

        for table in self.tables:
            imports.add_collection(table.async_imports if is_async else table.sync_imports)

        content = imports.formatted_imports
        content += '\n'

        content += '\n\n'.join(t.text_content(is_async) for t in self.tables)
        content += '\n'
        return content

    @property
    def init_strings(self) -> list[str]:
        return [
            EntityImport(
                name=self.file_name_sync,
                type=ImportType.relative,
                imports=[self.name_sync]
            ).import_string,
            EntityImport(
               name=self.file_name_async,
               type=ImportType.relative,
               imports=[self.name_async]
            ).import_string,
        ]

    @property
    def file_name(self) -> str:
        return StringUtils.camel_to_snake(self.manifest_class_name)

    @property
    def file_name_sync(self) -> str:
        return f'{self.file_name}_sync'

    @property
    def file_name_async(self) -> str:
        return f'{self.file_name}_async'

    @property
    def name_sync(self) -> str:
        return f'{self.manifest_class_name}Sync'

    @property
    def name_async(self) -> str:
        return f'{self.manifest_class_name}Async'

    @property
    def async_imports(self) -> EntityImportCollection:
        return EntityImportCollection([
            EntityImport(
                name=self.manifest_tables_path,
                type=ImportType.relative,
                imports=[t.async_name for t in self.tables]
            ),
            EntityImport(
                name='client_async',
                type=ImportType.relative,
                imports=['BungieClientAsync'],
                type_check=True,
            ),
            EntityImport(name='os', type=ImportType.stdlib),
            EntityImport(name='zipfile', type=ImportType.stdlib),
            EntityImport(name='typing', type=ImportType.stdlib, imports=['Any']),
            EntityImport(name='datetime', type=ImportType.stdlib, imports=['datetime', 'timedelta']),
            EntityImport(name='aiosqlite', type=ImportType.external),
        ])

    @property
    def sync_imports(self) -> EntityImportCollection:
        return EntityImportCollection([
            EntityImport(
                name=self.manifest_tables_path,
                type=ImportType.relative,
                imports=[t.sync_name for t in self.tables]
            ),
            EntityImport(
                name='client_sync',
                type=ImportType.relative,
                imports=['BungieClientSync'],
                type_check=True,
            ),
            EntityImport(name='os', type=ImportType.stdlib),
            EntityImport(name='zipfile', type=ImportType.stdlib),
            EntityImport(name='typing', type=ImportType.stdlib, imports=['Any']),
            EntityImport(name='datetime', type=ImportType.stdlib, imports=['datetime', 'timedelta']),
            EntityImport(name='sqlite3', type=ImportType.stdlib),
        ])

    def imports(self, is_async) -> EntityImportCollection:
        if is_async:
            return self.async_imports
        else:
            return self.sync_imports

    def init_method(self, is_async: bool) -> list[str]:
        items = [
            StringUtils.gen_function_declaration(
                func_name='__init__',
                params=[
                    'self',
                    f'bungie_client: \'{"BungieClientAsync" if is_async else "BungieClientSync"}\'',
                    'update_interval_minutes: int = 3600',
                    'locale: str = \'en\'',
                ],
                response_type='None',
            ),
            StringUtils.indent_str('self.bungie_client = bungie_client', 1),
            StringUtils.indent_str('self.update_interval_minutes = update_interval_minutes or 3600', 1),
            StringUtils.indent_str(
                'self._manifest_folder = \'\\\\\'.join(__file__.split(\'\\\\\')[:-1] + [\'\\\\manifest_data\'])',
                1
            ),
            StringUtils.indent_str('self.locale = locale or \'en\'\n', 1),
        ]
        items += [
            StringUtils.indent_str(f'self.{t.file_name} = {t.async_name if is_async else t.sync_name}(self)', 1)
            for t in self.tables
        ]

        return items

    @property
    def mobile_content_file_name_property(self) -> list[str]:
        return [
            '@property',
            StringUtils.gen_function_declaration('mobile_content_file_name', ['self'], 'str'),
            StringUtils.indent_str(
                'return f\'{self._manifest_mobile_content}_{self.locale}{self._manifest_ext}\'',
                1,
            )
        ]

    @property
    def mobile_content_file_property(self) -> list[str]:
        return [
            '@property',
            StringUtils.gen_function_declaration('mobile_content_file', ['self'], 'str | None'),
            StringUtils.indent_str('if self._manifest_version:', 1),
            StringUtils.indent_str(
                'return os.path.join(self._manifest_folder, self._manifest_version, self.mobile_content_file_name)',
                2,
            ),
        ]

    @staticmethod
    def get_manifest_method(is_async: bool) -> list[str]:
        return [
            StringUtils.gen_function_declaration(
                func_name='_get_manifest',
                params=['self'],
                response_type='None',
                is_async=is_async,
            ),
            StringUtils.indent_str(
                'if self._manifest_updated is None or datetime.utcnow() > '
                'self._manifest_updated + timedelta(hours=self.update_interval_minutes):',
                1
            ),
            StringUtils.indent_str(
                f'manifest_paths = {"await " if is_async else ""}self.bungie_client.destiny2.get_destiny_manifest()\n',
                2,
            ),
            StringUtils.indent_str('self._manifest_version = manifest_paths.Response.version', 2),
            StringUtils.indent_str('self._clean_data_folder()\n', 2),
            StringUtils.indent_str('if not self._manifest_version_exists():', 2),
            StringUtils.indent_str(
                'if not os.path.exists(os.path.join(self._manifest_folder, self._manifest_version)):',
                3,
            ),
            StringUtils.indent_str('os.mkdir(os.path.join(self._manifest_folder, self._manifest_version))\n', 4),
            StringUtils.indent_str('if self.locale not in manifest_paths.Response.mobileWorldContentPaths:', 3),
            StringUtils.indent_str(
                'raise ValueError(f\'The provided locale is not valid: \\\'{self.locale}\\\'\')\n',
                4,
            ),
            StringUtils.indent_str(
                'mobile_content_path = manifest_paths.Response.mobileWorldContentPaths[self.locale]',
                3,
            ),
            StringUtils.indent_str(
                f'content = {"await " if is_async else ""}self.bungie_client.get_file(mobile_content_path)\n',
                3,
            ),
            StringUtils.indent_str('with open(os.path.join(', 3),
            StringUtils.indent_str('self._manifest_folder,', 5),
            StringUtils.indent_str('self._manifest_version,', 5),
            StringUtils.indent_str('\'tmp.content\',', 5),
            StringUtils.indent_str('), \'wb+\') as f:', 3),
            StringUtils.indent_str('f.write(content)\n', 4),
            StringUtils.indent_str('with zipfile.ZipFile(os.path.join(', 3),
            StringUtils.indent_str('self._manifest_folder,', 5),
            StringUtils.indent_str('self._manifest_version,', 5),
            StringUtils.indent_str('\'tmp.content\',', 5),
            StringUtils.indent_str(')) as f:', 3),
            StringUtils.indent_str('name = f.namelist()', 4),
            StringUtils.indent_str('f.extractall(os.path.join(self._manifest_folder, self._manifest_version))\n', 4),
            StringUtils.indent_str('os.rename(', 3),
            StringUtils.indent_str('os.path.join(self._manifest_folder, self._manifest_version, name[0]),', 4),
            StringUtils.indent_str(
                'os.path.join(self._manifest_folder, self._manifest_version, self.mobile_content_file_name)',
                4,
            ),
            StringUtils.indent_str(')', 3),
            StringUtils.indent_str(
                'os.remove(os.path.join(self._manifest_folder, self._manifest_version, \'tmp.content\'))\n',
                3
            ),
            StringUtils.indent_str('self._manifest_updated = datetime.utcnow()', 2),
        ]

    @staticmethod
    def manifest_version_exists_method() -> list[str]:
        return [
            StringUtils.gen_function_declaration(
                '_manifest_version_exists',
                ['self'],
                'bool'
            ),
            StringUtils.indent_str(
                'if os.path.exists(os.path.join(self._manifest_folder, self._manifest_version)):',
                1,
            ),
            StringUtils.indent_str('return True', 2),
            StringUtils.indent_str('return False', 1),
        ]

    @staticmethod
    def clean_data_folder_method() -> list[str]:
        return [
            StringUtils.gen_function_declaration(
                '_clean_data_folder',
                ['self'],
                'None'
            ),
            StringUtils.indent_str('if not os.path.exists(self._manifest_folder):', 1),
            StringUtils.indent_str('os.mkdir(self._manifest_folder)', 2),
            StringUtils.indent_str('for p in os.listdir(self._manifest_folder):', 1),
            StringUtils.indent_str('if not p == self._manifest_version:', 2),
            StringUtils.indent_str('os.remove(os.path.join(self._manifest_folder, p))', 3),
        ]

    @staticmethod
    def query_method(is_async: bool) -> list[str]:
        if is_async:
            return [
                StringUtils.gen_function_declaration(
                    '_query',
                    ['self', 'path: str', 'query: str', 'many: bool = False', 'limit: int = None'],
                    'dict[str, Any] | list[dict[str, Any]]',
                    is_async=True,
                ),
                StringUtils.indent_str('async with aiosqlite.connect(path) as conn:', 1),
                StringUtils.indent_str('conn.row_factory = aiosqlite.Row', 2),
                StringUtils.indent_str('async with conn.execute(query) as cur:', 2),
                StringUtils.indent_str('if many:', 3),
                StringUtils.indent_str('if limit:', 4),
                StringUtils.indent_str('return [dict(r) for r in await cur.fetchmany(limit)]', 5),
                StringUtils.indent_str('else:', 4),
                StringUtils.indent_str('return [dict(r) for r in await cur.fetchall()]', 5),
                StringUtils.indent_str('else:', 3),
                StringUtils.indent_str('return dict(await cur.fetchone())', 4),
            ]
        else:
            return [
                StringUtils.gen_function_declaration(
                    '_query',
                    ['self', 'path: str', 'query: str', 'many: bool = False', 'limit: int = None'],
                    'dict[str, Any] | list[dict[str, Any]]',
                    is_async=False,
                ),
                StringUtils.indent_str('con = sqlite3.connect(path)', 1),
                StringUtils.indent_str('cur = con.cursor()', 1),
                StringUtils.indent_str('res = cur.execute(query)', 1),
                StringUtils.indent_str('if many:', 1),
                StringUtils.indent_str('if limit:', 2),
                StringUtils.indent_str('res = [dict(r) for r in res.fetchmany(limit)]', 3),
                StringUtils.indent_str('else:', 2),
                StringUtils.indent_str('res = [dict(r) for r in res.fetchall()]', 3),
                StringUtils.indent_str('else:', 1),
                StringUtils.indent_str('res = dict(res.fetchone())', 2),
                StringUtils.indent_str('cur.close()', 1),
                StringUtils.indent_str('con.close()', 1),
                StringUtils.indent_str('return res', 1),
            ]

    @staticmethod
    def query_mobile_content_method(is_async: bool) -> list[str]:
        return [
            StringUtils.gen_function_declaration(
                'query_mobile_content',
                ['self', 'query: str', 'many: bool = False', 'limit: int = None'],
                'dict[str, Any] | list[dict[str, Any]]',
                is_async=is_async,
            ),
            StringUtils.indent_str(f'{"await " if is_async else ""}self._get_manifest()', 1),
            StringUtils.indent_str(
                f'return {"await " if is_async else ""}self._query(self.mobile_content_file, query, many, limit)',
                1,
            ),
        ]

    def text_content(self, is_async: bool) -> str:
        content = self.imports(is_async).formatted_imports
        content += '\n'

        content += StringUtils.gen_class_declaration(class_name=self.name_async if is_async else self.name_sync)
        content += '\n'

        content += StringUtils.indent_str('_manifest_updated: datetime = None\n', 1)
        content += StringUtils.indent_str('_manifest_version: str = None\n', 1)
        content += StringUtils.indent_str('_manifest_mobile_content: str = \'MobileContent\'\n', 1)
        content += StringUtils.indent_str('_manifest_ext: str = \'.db\'\n', 1)
        content += '\n'

        content += '\n'.join(StringUtils.indent_str(l, 1) for l in self.init_method(is_async))
        content += '\n\n'

        content += '\n'.join(StringUtils.indent_str(l, 1) for l in self.mobile_content_file_name_property)
        content += '\n\n'

        content += '\n'.join(StringUtils.indent_str(l, 1) for l in self.mobile_content_file_property)
        content += '\n\n'

        content += '\n'.join(StringUtils.indent_str(l, 1) for l in self.get_manifest_method(is_async))
        content += '\n\n'

        content += '\n'.join(StringUtils.indent_str(l, 1) for l in self.manifest_version_exists_method())
        content += '\n\n'

        content += '\n'.join(StringUtils.indent_str(l, 1) for l in self.clean_data_folder_method())
        content += '\n\n'

        content += '\n'.join(StringUtils.indent_str(l, 1) for l in self.query_method(is_async))
        content += '\n\n'

        content += '\n'.join(StringUtils.indent_str(l, 1) for l in self.query_mobile_content_method(is_async))
        content += '\n'
        return content

    def write(self, folder: str) -> None:
        if not os.path.exists(os.path.join(folder, self.manifest_tables_path)):
            os.mkdir(os.path.join(folder, self.manifest_tables_path))

        with open(os.path.join(
                folder,
                self.manifest_tables_path,
                self.manifest_tables_path + '_async' + self.file_extension
        ), 'w+') as f:
            f.write(self.tables_text_content(True))

        with open(os.path.join(
                folder,
                self.manifest_tables_path,
                self.manifest_tables_path + '_sync' + self.file_extension
        ), 'w+') as f:
            f.write(self.tables_text_content(False))

        with open(os.path.join(folder, self.file_name_async + self.file_extension), 'w+') as f:
            f.write(self.text_content(True))

        with open(os.path.join(folder, self.file_name_sync + self.file_extension), 'w+') as f:
            f.write(self.text_content(False))
