import os
from typing import Optional, Any

from .entity_import import EntityImportCollection, EntityImport
from .enums import ImportType, PropertyType
from .openapi.parameter import Parameter
from .openapi.path_item import PathItem
from .openapi.reference import Reference
from .openapi.schema import Schema
from .openapi.server import Server
from ..utils.str_utils import StringUtils


class EndpointParam:
    def __init__(self, name: str, required: bool = True, type: str = None, default: str = None, is_enum: bool = False) -> None:
        if required is None:
            required = False

        self.name = name
        self.required = required
        self.raw_type = type
        self.default = default
        self.is_enum = is_enum
        if self.is_enum:
            self._type = f'{type} | int'
        else:
            self._type = type

    @property
    def snake_name(self) -> str:
        return StringUtils.camel_to_snake(self.name)

    @property
    def type(self) -> str:
        if self._type:
            if self.required:
                return self._type
            else:
                return f'Optional[{self._type}]'

    @property
    def default_str(self) -> str:
        if not self.required:
            return f' = {self.default}'
        else:
            if self.default:
                return f' = {self.default}'

    @property
    def declaration(self) -> str:
        return f'{self.snake_name}{": " + self.type if self.type else ""}{self.default_str or ""}'

    @property
    def format_format(self) -> str:
        if not self.is_enum:
            return f'{self.name}={self.snake_name}'
        else:
            return f'{self.name}={self.snake_name}.value'


class Endpoint:
    response_type: Optional[str]
    # Mapping of parameter type (path, query, etc.) to a list of endpoint params
    parameters: dict[str, list[EndpointParam]]
    response_is_model: bool

    entities_path_name = 'entities'
    bungie_root_var = '{bungie_root}'

    def __init__(
            self,
            path: str,
            endpoint: PathItem,
            is_async: bool = False,
    ) -> None:
        self.path = path
        self.endpoint = endpoint
        self.is_async = is_async

        self.imports = EntityImportCollection()
        self.response_type = None
        self.parameters = {'core': [EndpointParam(name='self')]}
        self.response_is_model = False

        self.process_endpoint()

    @property
    def qualified_name(self) -> str:
        return self.endpoint.summary.strip('.')

    @property
    def description(self) -> str:
        return self.endpoint.description

    @property
    def get(self) -> bool:
        return self.endpoint.get is not None

    @property
    def post(self) -> bool:
        return self.endpoint.post is not None

    @property
    def all_params(self) -> list[EndpointParam]:
        params = []
        for ps in self.parameters.values():
            params += list(ps)
        return params

    @property
    def spec_params(self) -> list[Reference | Parameter]:
        if self.get:
            return self.endpoint.get.parameters
        elif self.post:
            return self.endpoint.post.parameters
        else:
            return []

    @property
    def enum_params(self) -> list[EndpointParam]:
        return [p for p in self.all_params if p.is_enum]

    @property
    def method(self) -> str:
        if self.get:
            return 'get'
        elif self.post:
            return 'post'
        else:
            return None

    @property
    def endpoint_name(self) -> str:
        return self.endpoint.summary.split('.')[-1]

    @property
    def func_name(self) -> str:
        return StringUtils.camel_to_snake(self.endpoint_name)

    @property
    def func_definition(self) -> str:
        required_params = []
        default_params = []
        optional_params = []

        for ps in self.parameters.values():
            for p in ps:
                if p.required:
                    if p.default:
                        default_params.append(p.declaration)
                    else:
                        required_params.append(p.declaration)
                else:
                    optional_params.append(p.declaration)

        return StringUtils.gen_function_declaration(
            func_name=self.func_name,
            params=required_params + default_params + optional_params,
            response_type=self.response_type,
            is_async=self.is_async,
            depth=1
        )

    @property
    def endpoint_body(self) -> str:
        content = ''
        # Enum validation
        if self.enum_params:
            for p in self.enum_params:
                content += StringUtils.indent_str(f'if isinstance({p.snake_name}, int):\n', 2)
                content += StringUtils.indent_str(f'{p.snake_name} = {p.raw_type}({p.snake_name})\n', 3)
            content += '\n'

        if not self.is_async:
            # Sync body
            content += StringUtils.indent_str(f'raw = self._parent._{self.method}(\n', 2)
            content += StringUtils.indent_str(f'\'{self.bungie_root_var}{self.path}\'.format(\n', 3)
            content += StringUtils.indent_str('bungie_root=self._bungie_root,\n', 4)
            content += '\n'.join(StringUtils.indent_str(p.format_format, 4) + ',' for p in self.parameters.get('path', []))
            content += '\n' if self.parameters.get('path') else ''
            content += StringUtils.indent_str('),\n', 3)
            content += StringUtils.indent_str(')\n', 2)
            content += StringUtils.indent_str(f'return {self.response_type}.schema().loads(raw)', 2)
        else:
            # Async body
            content += StringUtils.indent_str(f'raw = await self._parent._{self.method}(\n', 2)
            content += StringUtils.indent_str(f'\'{self.bungie_root_var}{self.path}\'.format(\n', 3)
            content += StringUtils.indent_str('bungie_root=self._bungie_root,\n', 4)
            content += '\n'.join(
                StringUtils.indent_str(p.format_format, 4) + ',' for p in self.parameters.get('path', []))
            content += '\n' if self.parameters.get('path') else ''
            content += StringUtils.indent_str('),\n', 3)
            content += StringUtils.indent_str(')\n', 2)
            content += StringUtils.indent_str(f'return {self.response_type}.schema().loads(raw)', 2)
        return content

    @property
    def formatted_endpoint(self) -> str:
        content = self.func_definition
        content += '\n'
        content += StringUtils.gen_docstring(self.description, 2)
        content += '\n'
        # TODO: ADD FUNCTION BODY
        content += self.endpoint_body
        return content

    def process_endpoint(self) -> None:
        if self.get:
            response = self.endpoint.get.responses['200']
            if response.ref:
                self.response_type = StringUtils.get_class_name_from_ref_str(response.ref)
                self.imports.add_import(EntityImport(
                    name=f'.{self.entities_path_name}',
                    type=ImportType.relative,
                    imports=[self.response_type]
                ))
                self.response_is_model = True
            else:
                print(f'UNHANDLED RESPONSE TYPE: {self.endpoint_name} - {response}')
            self.process_parameters()
        else:
            print(f'UNHANDLED ENDPOINT: {self.endpoint_name} - {self.endpoint}')

    def get_type_from_param_schema(self, schema: Schema) -> tuple[str, bool]:
        t = PropertyType(schema.type)
        if t not in [PropertyType.object, PropertyType.array, PropertyType.string, PropertyType.integer]:
            return t.python_type, False
        elif t == PropertyType.integer:
            if schema.x_enum_reference:
                ref_name = StringUtils.get_class_name_from_ref_str(schema.x_enum_reference.ref)
                self.imports.add_import(EntityImport(
                    name=f'.{self.entities_path_name}',
                    type=ImportType.relative,
                    imports=[ref_name]
                ))
                return ref_name, True
            else:
                return t.python_type, False
        else:
            print(f'UNHANDLED PARAM SCHEMA TYPE: {self.endpoint_name} - {schema}')
            self.imports.add_import(EntityImport(name='typing', type=ImportType.stdlib, imports=['Any']))
            return 'Any', False

    def gen_param(self, parameter: Parameter) -> EndpointParam:
        t, is_enum = self.get_type_from_param_schema(parameter.schema)
        param = EndpointParam(
            name=parameter.name,
            required=parameter.required or False,
            type=t,
            default=parameter.schema.default,
            is_enum=is_enum,
        )
        return param

    def process_parameters(self) -> None:
        for parameter in self.spec_params:
            if parameter.in_ == 'path':
                if 'path' not in self.parameters:
                    self.parameters['path'] = []
                if isinstance(parameter, Parameter):
                    if not parameter.required:
                        self.imports.add_import(EntityImport(
                            name='typing',
                            type=ImportType.stdlib,
                            imports=['Optional']
                        ))
                    self.parameters['path'].append(self.gen_param(parameter))
                else:
                    print(f'UNHANDLED PATH REF PARAM: {self.endpoint_name} - {parameter}')
            elif parameter.in_ == 'query':
                if 'query' not in self.parameters:
                    self.parameters['query'] = []
                if isinstance(parameter, Parameter):
                    if not parameter.required:
                        self.imports.add_import(EntityImport(
                            name='typing',
                            type=ImportType.stdlib,
                            imports=['Optional']
                        ))
                    self.parameters['query'].append(self.gen_param(parameter))
                else:
                    print(f'UNHANDLED QUERY REF PARAM: {self.endpoint_name} - {parameter}')
            else:
                print(f'UNHANDLED PARAMETER: {self.endpoint_name} - {parameter.name} - {parameter}')


class EndpointCollection:
    entity_path_name = 'entities'
    endpoints_path_name = 'endpoints'
    file_extension = '.py'
    sync_client_name = 'BungieClientSync'
    async_client_name = 'BungieClientAsync'
    sync_client_file_name = 'client_sync'
    async_client_file_name = 'client_async'

    sync_endpoints: list[Endpoint]
    async_endpoints: list[Endpoint]

    def __init__(self, name: str, bungie_root: Server):
        self.name = name
        self.bungie_root = bungie_root
        self.sync_imports = EntityImportCollection([
            EntityImport(
                name='requests',
                type=ImportType.external,
            ),
            EntityImport(
                name=f'.{self.sync_client_file_name}',
                type=ImportType.relative,
                imports=[self.sync_client_name],
                type_check=True,
            ),
        ])
        self.async_imports = EntityImportCollection([
            EntityImport(
                name='aiohttp',
                type=ImportType.external,
            ),
            EntityImport(
                name=f'.{self.async_client_file_name}',
                type=ImportType.relative,
                imports=[self.async_client_name],
                type_check=True,
            ),
        ])
        self.sync_endpoints = []
        self.async_endpoints = []

    @property
    def name_sync(self) -> str:
        return f'{self.name}Sync'

    @property
    def name_async(self) -> str:
        return f'{self.name}Async'

    @property
    def var_name(self) -> str:
        return StringUtils.camel_to_snake(self.name)

    @property
    def file_name_sync(self) -> str:
        return StringUtils.camel_to_snake(self.name_sync)

    @property
    def file_name_async(self) -> str:
        return StringUtils.camel_to_snake(self.name_async)

    @property
    def init_import_sync(self) -> str:
        return EntityImport(
            name=self.file_name_sync,
            type=ImportType.relative,
            imports=[self.name_sync],
        ).import_string

    @property
    def init_import_async(self) -> str:
        return EntityImport(
            name=self.file_name_async,
            type=ImportType.relative,
            imports=[self.name_async],
        ).import_string

    @property
    def init_imports(self) -> EntityImportCollection:
        return EntityImportCollection([
            EntityImport(
                name=self.file_name_sync,
                type=ImportType.relative,
                imports=[self.name_sync],
            ),
            EntityImport(
                name=self.file_name_async,
                type=ImportType.relative,
                imports=[self.name_async],
            ),
        ])

    @property
    def standard_content(self) -> str:
        content = StringUtils.gen_comment(self.bungie_root.description, 1)
        content += '\n'
        content += StringUtils.indent_str(f'_bungie_root: str = \'{self.bungie_root.url}\'', 1)
        return content

    @property
    def text_content_sync(self) -> str:
        content = self.sync_imports.formatted_imports
        content += '\n'
        content += StringUtils.gen_class_declaration(self.name_sync)
        content += '\n'
        content += self.standard_content
        content += '\n\n'
        content += StringUtils.indent_str(f'def __init__(self, parent: \'{self.sync_client_name}\'):\n', 1)
        content += StringUtils.indent_str('self._parent = parent', 2)
        content += '\n\n'
        content += '\n\n'.join(e.formatted_endpoint for e in self.sync_endpoints)
        content += '\n'
        return content

    @property
    def text_content_async(self) -> str:
        content = self.async_imports.formatted_imports
        content += '\n'
        content += StringUtils.gen_class_declaration(self.name_async)
        content += '\n'
        content += self.standard_content
        content += '\n\n'
        content += StringUtils.indent_str(f'def __init__(self, parent: \'{self.async_client_name}\'):\n', 1)
        content += StringUtils.indent_str('self._parent = parent', 2)
        content += '\n\n'
        content += '\n\n'.join(e.formatted_endpoint for e in self.async_endpoints)
        content += '\n'
        return content

    def add_endpoint(self, path: str, endpoint: PathItem) -> None:
        sync_endpoint = Endpoint(path, endpoint, False)
        self.sync_endpoints.append(sync_endpoint)
        self.sync_imports.add_collection(sync_endpoint.imports)

        async_endpoint = Endpoint(path, endpoint, True)
        self.async_endpoints.append(async_endpoint)
        self.async_imports.add_collection(async_endpoint.imports)

    def write_files(self, folder: str) -> None:
        with open(os.path.join(folder, self.file_name_sync + self.file_extension), 'w+') as endpoint_file:
            endpoint_file.write(self.text_content_sync)

        with open(os.path.join(folder, self.file_name_async + self.file_extension), 'w+') as endpoint_file:
            endpoint_file.write(self.text_content_async)
