import os
from typing import Optional

from .entity import Entity, EntityCollection
from .entity_import import EntityImportCollection, EntityImport
from .enums import ImportType, PropertyType, PropertyFormat
from .openapi.parameter import Parameter
from .openapi.path_item import PathItem
from .openapi.reference import Reference
from .openapi.request_body import RequestBody
from .openapi.schema import Schema
from .openapi.server import Server
from ..utils.str_utils import StringUtils


class EndpointParam:
    def __init__(
            self,
            name: str,
            required: bool = True,
            type: str = None,
            default: str = None,
            is_enum: bool = False,
            is_datetime: bool = False,
            is_array: bool = False,
            from_body: bool = False,
    ) -> None:
        if required is None:
            required = False

        self.name = name
        self.required = required
        self.raw_type = type
        self.default = default
        self.is_enum = is_enum
        self.is_datetime = is_datetime
        self.is_array = is_array
        self.from_body = from_body

        if type:
            self._type = ''
            if self.is_array:
                self._type += 'list['
            if self.is_enum:
                self._type += f'{type} | int'
            elif self.is_datetime:
                self._type += f'{type} | str'
            else:
                self._type += type
            if self.is_array:
                self._type += ']'
        else:
            if self.is_array:
                self._type = 'list'
            elif self.is_enum:
                self._type = 'int'
            elif self.is_datetime:
                self._type = 'str'
            else:
                self._type = None

    @property
    def snake_name(self) -> str:
        return StringUtils.camel_to_snake(self.name)

    @property
    def type(self) -> str:
        if self._type:
            if not self.required:  # and not self.from_body:
                return f'Optional[{self._type}]'
            else:
                return self._type

    @property
    def default_str(self) -> str:
        if not self.required:  # and not self.from_body:
            return f' = {self.default}'
        else:
            if self.default:
                return f' = {self.default}'

    @property
    def declaration(self) -> str:
        return f'{self.snake_name}{": " + self.type if self.type else ""}{self.default_str or ""}'

    @property
    def format_format(self) -> str:
        return f'{self.name}={self.value}'

    @property
    def value(self) -> str:
        if self.is_enum:
            if self.is_array:
                return f'\',\'.join(str(e.value) for e in {self.snake_name})'
            else:
                return f'{self.snake_name}.value'
        elif self.is_datetime:
            return f'{self.snake_name}.isoformat()'
        else:
            return self.snake_name


class Endpoint:
    response_type: Optional[str]
    # Mapping of parameter type (path, query, etc.) to a list of endpoint params
    parameters: dict[str, list[EndpointParam]]
    response_is_model: bool
    request_body_entity: Entity | None
    array_body_type: str | None
    requires_oauth: bool
    oauth_scopes: list[str] | None

    entities_path_name = 'entities'
    bungie_root_var = '{bungie_root}'

    response_type_overrides = {
        'get_destiny_entity_definition': 'entity_type'
    }

    def __init__(
            self,
            path: str,
            endpoint: PathItem,
            entities: EntityCollection,
            is_async: bool = False,
    ) -> None:
        self.path = path
        self.endpoint = endpoint
        self.entities = entities
        self.is_async = is_async

        self.imports = EntityImportCollection()
        self.response_type = None
        self.parameters = {'core': [EndpointParam(name='self')]}
        self.response_is_model = False
        self.request_body_entity = None
        self.array_body_type = None
        self.requires_oauth = False
        self.oauth_scopes = None

        self.process_endpoint()

    @property
    def qualified_name(self) -> str:
        return self.endpoint.summary.strip('.')

    @property
    def description(self) -> str:
        desc = self.endpoint.description

        if self.is_preview:
            desc += '\n\n'
            desc += 'DISCLAIMER: This endpoint is a preview endpoint and may undergo frequent updates/changes and ' \
                    'have incomplete data structures.'

        if self.requires_oauth:
            desc += '\n\n'
            desc += f'Requires OAuth Scopes:\n'
            desc += f'- {", ".join(self.oauth_scopes)}'
        return desc

    @property
    def get(self) -> bool:
        return self.endpoint.get is not None

    @property
    def post(self) -> bool:
        return self.endpoint.post is not None

    @property
    def is_preview(self) -> bool:
        if self.get:
            return bool(self.endpoint.get.x_preview)
        elif self.post:
            return bool(self.endpoint.post.x_preview)
        else:
            return False

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
    def request_body(self) -> RequestBody:
        if self.get:
            return self.endpoint.get.requestBody
        elif self.post:
            return self.endpoint.post.requestBody
        else:
            return None

    @property
    def enum_params(self) -> list[EndpointParam]:
        return [p for p in self.all_params if p.is_enum and not p.is_array and not p.from_body]

    @property
    def datetime_params(self) -> list[EndpointParam]:
        return [p for p in self.all_params if p.is_datetime and not p.from_body]

    @property
    def array_enum_params(self) -> list[EndpointParam]:
        return [p for p in self.all_params if p.is_enum and p.is_array and not p.from_body]

    @property
    def body_params(self) -> list[EndpointParam]:
        return [p for p in self.all_params if p.from_body]

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
            content += StringUtils.gen_comment('Enum parameter validation.', 2)
            content += '\n'
            for p in self.enum_params:
                content += StringUtils.indent_str(f'if isinstance({p.snake_name}, int):\n', 2)
                content += StringUtils.indent_str(f'{p.snake_name} = {p.raw_type}({p.snake_name})\n', 3)
            content += '\n'
        if self.datetime_params:
            content += StringUtils.gen_comment('Datetime parameter validation.', 2)
            content += '\n'
            for p in self.datetime_params:
                content += StringUtils.indent_str(f'if isinstance({p.snake_name}, str):\n', 2)
                content += StringUtils.indent_str(f'{p.snake_name} = datetime.fromisoformat({p.snake_name})\n', 3)
            content += '\n'
        if self.array_enum_params:
            content += StringUtils.gen_comment('Enum list validation.', 2)
            content += '\n'
            for p in self.array_enum_params:
                content += StringUtils.indent_str(f'if {p.snake_name}:\n', 2)
                content += StringUtils.indent_str('tmp = []\n', 3)
                content += StringUtils.indent_str(f'for e in {p.snake_name}:\n', 3)
                content += StringUtils.indent_str(f'if isinstance(e, int):\n', 4)
                content += StringUtils.indent_str(f'tmp.append({p.raw_type}(e))\n', 5)
                content += StringUtils.indent_str(f'else:\n', 4)
                content += StringUtils.indent_str(f'tmp.append(e)\n', 5)
                content += StringUtils.indent_str(f'{p.snake_name} = tmp\n', 3)
            content += '\n'

        if self.parameters.get('query'):
            content += StringUtils.gen_comment('Query parameters', 2)
            content += '\n'
            content += StringUtils.indent_str('_params = {}\n', 2)
            for p in self.parameters.get('query'):
                content += StringUtils.indent_str(f'if {p.snake_name}:\n', 2)
                content += StringUtils.indent_str(f'_params[\'{p.name}\'] = {p.value}\n', 3)
            content += '\n'

        if self.body_params:
            if self.request_body_entity:
                content += StringUtils.gen_comment('Request body parameters', 2)
                content += '\n'
                content += StringUtils.indent_str(f'_entity = {self.request_body_entity if isinstance(self.request_body_entity, str) else self.request_body_entity.name_safe}(\n', 2)
                for p in self.body_params:
                    content += StringUtils.indent_str(f'{p.name}={p.snake_name},\n', 3)
                content += StringUtils.indent_str(f')\n', 2)

        content += StringUtils.gen_comment('Make the request', 2)
        content += '\n'
        if not self.is_async:
            # Sync body
            content += StringUtils.indent_str(f'{"raw = " if self.response_type else ""}self._parent._{self.method}(\n', 2)
        else:
            # Async body
            content += StringUtils.indent_str(f'{"raw = " if self.response_type else ""}await self._parent._{self.method}(\n', 2)

        # Arguments are the same
        content += StringUtils.indent_str(f'\'{self.bungie_root_var}{self.path}\'.format(\n', 3)
        content += StringUtils.indent_str('bungie_root=self._bungie_root,\n', 4)
        content += '\n'.join(
            StringUtils.indent_str(p.format_format, 4) + ',' for p in self.parameters.get('path', []))
        content += '\n' if self.parameters.get('path') else ''
        content += StringUtils.indent_str('),\n', 3)

        if self.parameters.get('query'):
            content += StringUtils.indent_str('params=_params if _params else None,\n', 3)
        if self.body_params:
            content += StringUtils.indent_str('headers={\'Content-Type\': \'application/json\'},\n', 3)

            if self.request_body_entity:
                content += StringUtils.indent_str(
                    f'json={self.request_body_entity if isinstance(self.request_body_entity, str) else self.request_body_entity.name_safe}.schema().dump(_entity),\n',
                    3
                )
            elif self.array_body_type:
                content += StringUtils.indent_str('json=values,\n', 3)
        if self.requires_oauth:
            content += StringUtils.indent_str('requires_oauth=True,\n', 3)

        content += StringUtils.indent_str(')', 2)

        if self.response_type:
            content += '\n\n'
            content += StringUtils.gen_comment('Validate response', 2)
            content += '\n'
            if self.func_name in self.response_type_overrides:
                content += StringUtils.indent_str(
                    f'return globals()[{self.response_type_overrides[self.func_name]}].schema().loads(raw)',
                    2
                )
            else:
                content += StringUtils.indent_str(f'return {self.response_type}.schema().loads(raw)', 2)

        return content

    @property
    def formatted_endpoint(self) -> str:
        content = self.func_definition
        content += '\n'
        content += StringUtils.gen_docstring(self.description, 2)
        content += '\n'
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
                if self.endpoint.get.security:
                    for security in self.endpoint.get.security:
                        for t, scopes in security.items():
                            if t == 'oauth2':
                                self.requires_oauth = True
                                self.oauth_scopes = scopes
                            else:
                                print(f'UNHANDLED SECURITY TYPE: {self.endpoint_name} - {t}')
            else:
                print(f'UNHANDLED RESPONSE TYPE: {self.endpoint_name} - {response}')
            self.process_parameters()
        elif self.post:
            response = self.endpoint.post.responses['200']
            if response.ref:
                self.response_type = StringUtils.get_class_name_from_ref_str(response.ref)
                self.imports.add_import(EntityImport(
                    name=f'.{self.entities_path_name}',
                    type=ImportType.relative,
                    imports=[self.response_type]
                ))
                self.response_is_model = True
                self.process_request_body()
                if self.endpoint.post.security:
                    for security in self.endpoint.post.security:
                        for t, scopes in security.items():
                            if t == 'oauth2':
                                self.requires_oauth = True
                                self.oauth_scopes = scopes
                            else:
                                print(f'UNHANDLED SECURITY TYPE: {self.endpoint_name} - {t}')
            else:
                print(f'UNHANDLED RESPONSE TYPE: {self.endpoint_name} - {response}')
            self.process_parameters()
        else:
            print(f'UNHANDLED ENDPOINT: {self.endpoint_name} - {self.endpoint}')

    def gen_param(self, parameter: Parameter) -> EndpointParam:
        is_enum = False
        is_datetime = False
        is_array = False
        tp = None
        schema = parameter.schema
        t = PropertyType(schema.type)
        if t in [PropertyType.boolean, PropertyType.number]:
            tp = t.python_type
        elif t == PropertyType.integer:
            if schema.x_enum_reference:
                ref_name = StringUtils.get_class_name_from_ref_str(schema.x_enum_reference.ref)
                self.imports.add_import(EntityImport(
                    name=f'.{self.entities_path_name}',
                    type=ImportType.relative,
                    imports=[ref_name]
                ))
                tp = ref_name
                is_enum = True
            else:
                tp = t.python_type
        elif t == PropertyType.string:
            fmt = PropertyFormat(schema.format)
            if fmt == PropertyFormat.none:
                tp = PropertyType.string.python_type
            elif fmt == PropertyFormat.datetime:
                self.imports.add_import(EntityImport(
                    name='datetime',
                    type=ImportType.stdlib,
                    imports=['datetime']
                ))
                tp = 'datetime'
                is_datetime = True
            else:
                print(f'UNHANDLED STRING TYPE: {self.endpoint_name} - {parameter.name} - {fmt} - {schema}')
        elif t == PropertyType.array:
            is_array = True
            if schema.items.x_enum_reference:
                ref_name = StringUtils.get_class_name_from_ref_str(schema.items.x_enum_reference.ref)
                self.imports.add_import(EntityImport(
                    name=f'.{self.entities_path_name}',
                    type=ImportType.relative,
                    imports=[ref_name]
                ))
                tp = ref_name
                is_enum = True
            else:
                print(f'UNHANDLED ARRAY TYPE: {self.endpoint_name} - {parameter.name} - {schema}')
        else:
            print(f'UNHANDLED PARAM SCHEMA TYPE: {self.endpoint_name} - {schema}')
            self.imports.add_import(EntityImport(name='typing', type=ImportType.stdlib, imports=['Any']))
            tp = 'Any'

        param = EndpointParam(
            name=parameter.name,
            required=parameter.required or False,
            type=tp,
            default=parameter.schema.default,
            is_enum=is_enum,
            is_datetime=is_datetime,
            is_array=is_array,
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

    def set_request_body(self, entity: Entity) -> None:
        for prop in entity.properties:
            if 'body' not in self.parameters:
                self.parameters['body'] = []
            if prop.optional:
                self.imports.add_import(EntityImport(
                    name='typing',
                    type=ImportType.stdlib,
                    imports=['Optional']
                ))
            if prop.enum or prop.forward_ref or any(s.isupper() for s in prop.type):
                self.imports.add_import(EntityImport(
                    name=f'.{self.entities_path_name}',
                    type=ImportType.relative,
                    imports=[prop.type]
                ))
            self.parameters['body'].append(EndpointParam(
                name=prop.name,
                required=not prop.optional,
                type=prop.field_type_required,
                from_body=True,
            ))
        self.imports.add_import(EntityImport(
            name=f'.{self.entities_path_name}',
            type=ImportType.relative,
            imports=[entity.name_safe]
        ))
        self.request_body_entity = entity

    def set_array_request_body(self, type: str) -> None:
        if 'body' not in self.parameters:
            self.parameters['body'] = []
        self.array_body_type = f'list[{type}]'
        self.parameters['body'].append(EndpointParam(
            name='values',
            type=type,
            is_array=True,
            from_body=True,
        ))

    def process_request_body(self) -> None:
        if self.request_body:
            content = self.request_body.content
            for c_type, media in content.items():
                if c_type == 'application/json':
                    if isinstance(media.schema, Reference):
                        ref_name = StringUtils.get_class_name_from_ref_str(media.schema.ref)
                        for e in self.entities.entities:
                            if e.name_safe == ref_name:
                                self.set_request_body(e)
                                break
                        if 'body' not in self.parameters:
                            print(f'REF NAME NOT FOUND: {self.endpoint_name} - {ref_name} - {media}')
                    elif isinstance(media.schema, Schema):
                        if PropertyType(media.schema.type) == PropertyType.array:
                            tp = PropertyType(media.schema.items.type)
                            if tp == PropertyType.integer and not media.schema.items.x_enum_reference:
                                self.set_array_request_body(tp.python_type)
                            else:
                                print(f'MEDIA SCHEMA ARRAY TYPE NOT HANDLED: {self.endpoint_name} - {tp} - {media}')
                        else:
                            print(f'MEDIA SCHEMA TYPE NOT HANDLED: {self.endpoint_name} - {media.schema.type} - {media}')
                    else:
                        print(f'MEDIA TYPE NOT HANDLED: {self.endpoint_name} - {media}')
                else:
                    print(f'UNHANDLED REQUEST BODY TYPE: {self.endpoint_name} - {c_type} - {self.request_body}')


class OAuthEndpoint:
    utils_path_name = 'utils'
    oauth_utils_name = 'oauth_utils'

    response_type = 'AccessToken'
    client_type_enum = 'OAuthClientType'

    refresh_token_meth = 'RefreshAccessToken'
    refresh_token_doc = 'Gets a new access token from a refresh token.'
    refresh_method = 'post'
    access_token_meth = 'GetAccessToken'
    access_token_doc = 'Gets a new access token from a authorization code.'
    access_method = 'post'

    def __init__(
            self,
            path: str,
            is_async: bool = False,
            is_refresh: bool = False,
    ) -> None:
        self.path = path
        self.is_async = is_async
        self.is_refresh = is_refresh

    @property
    def method(self) -> str:
        if self.is_refresh:
            return self.refresh_method
        else:
            return self.access_method

    @property
    def name(self) -> str:
        if self.is_refresh:
            return self.refresh_token_meth
        else:
            return self.access_token_meth

    @property
    def func_name(self) -> str:
        return StringUtils.camel_to_snake(self.name)

    @property
    def description(self) -> str:
        if self.is_refresh:
            return self.refresh_token_doc
        else:
            return self.access_token_doc

    @property
    def parameters(self) -> dict[str, list[EndpointParam]]:
        params = {'core': [EndpointParam(name='self')]}

        if self.is_refresh:
            params['core'].append(EndpointParam(name='refresh_token', type='str'))
        else:
            params['core'].append(EndpointParam(name='code', type='str'))

        return params

    @property
    def imports(self) -> EntityImportCollection:
        imps = EntityImportCollection([EntityImport(
            name=f'.{self.utils_path_name}.{self.oauth_utils_name}',
            type=ImportType.relative,
            imports=[self.response_type, self.client_type_enum, 'OAuthInformationNotProvided'],
        )])

        if self.is_async:
            imps.add_import(EntityImport(name='aiohttp', type=ImportType.external, imports=['BasicAuth']))
        else:
            imps.add_import(EntityImport(name='requests.auth', type=ImportType.external, imports=['HTTPBasicAuth']))

        return imps

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
            depth=1,
        )

    @property
    def endpoint_body(self) -> str:
        content = ''
        if self.is_refresh:
            content += StringUtils.indent_str('if not self._parent.oauth_type == OAuthClientType.Confidential:\n', 2)
            content += StringUtils.indent_str('raise OAuthInformationNotProvided(\n', 3)
            content += StringUtils.indent_str(
                '"You must provide a \'client_secret\' to the client \"\n',
                4,
            )
            content += StringUtils.indent_str('"in order to refresh an OAuth token."\n', 4)
        else:
            content += StringUtils.indent_str('if self._parent.oauth_type == OAuthClientType.NotApplicable:\n', 2)
            content += StringUtils.indent_str('raise OAuthInformationNotProvided(\n', 3)
            content += StringUtils.indent_str(
                '"You must provide a \'client_id\' and optionally a \'client_secret\' \"\n',
                4,
            )
            content += StringUtils.indent_str('"to the client in order to use OAuth endpoints."\n', 4)
        content += StringUtils.indent_str(')\n', 3)
        content += '\n'


        if self.is_refresh:
            content += StringUtils.indent_str('headers = {\n', 2)
            content += StringUtils.indent_str('\'Content-Type\': \'application/x-www-form-urlencoded\',\n', 3)
            content += StringUtils.indent_str('}\n', 2)
            content += StringUtils.indent_str('body = {\n', 2)
            content += StringUtils.indent_str('\'grant_type\': \'refresh_token\',\n', 3)
            content += StringUtils.indent_str('\'refresh_token\': refresh_token,\n', 3)
            content += StringUtils.indent_str('}\n', 2)
            if self.is_async:
                content += StringUtils.indent_str(
                    'auth = BasicAuth(str(self._parent.client_id), self._parent.client_secret)\n',
                    2
                )
                content += '\n'
                content += StringUtils.indent_str(f'raw = await self._parent._{self.method}(\n', 2)
            else:
                content += StringUtils.indent_str(
                    'auth = HTTPBasicAuth(str(self._parent.client_id), self._parent.client_secret)\n',
                    2
                )
                content += '\n'
                content += StringUtils.indent_str(f'raw = self._parent._{self.method}(\n', 2)
        else:
            content += StringUtils.indent_str('headers = {\n', 2)
            content += StringUtils.indent_str('\'Content-Type\': \'application/x-www-form-urlencoded\',\n', 3)
            content += StringUtils.indent_str('}\n', 2)
            content += StringUtils.indent_str('body = {\n', 2)
            content += StringUtils.indent_str('\'grant_type\': \'authorization_code\',\n', 3)
            content += StringUtils.indent_str('\'code\': code,\n', 3)
            content += StringUtils.indent_str('}\n', 2)
            content += StringUtils.indent_str('auth = None\n', 2)
            content += '\n'
            content += StringUtils.indent_str(f'if self._parent.oauth_type == {self.client_type_enum}.Public:\n', 2)
            content += StringUtils.indent_str('body.update({\'client_id\': self._parent.client_id})\n', 3)
            content += StringUtils.indent_str(
                f'elif self._parent.oauth_type == {self.client_type_enum}.Confidential:\n',
                2
            )
            if self.is_async:
                content += StringUtils.indent_str(
                    'auth = BasicAuth(str(self._parent.client_id), self._parent.client_secret)\n',
                    3
                )
                content += '\n'
                content += StringUtils.indent_str(f'raw = await self._parent._{self.method}(\n', 2)
            else:
                content += StringUtils.indent_str(
                    'auth = HTTPBasicAuth(str(self._parent.client_id), self._parent.client_secret)\n',
                    3
                )
                content += '\n'
                content += StringUtils.indent_str(f'raw = self._parent._{self.method}(\n', 2)
        content += StringUtils.indent_str(f'\'{self.path}\',\n', 3)
        content += StringUtils.indent_str(f'headers=headers,\n', 3)
        content += StringUtils.indent_str(f'data=body,\n', 3)
        content += StringUtils.indent_str(f'auth=auth,\n', 3)
        content += StringUtils.indent_str(')\n', 2)
        content += '\n'
        content += StringUtils.indent_str(f'return {self.response_type}.schema().loads(raw)', 2)
        return content

    @property
    def formatted_endpoint(self) -> str:
        content = self.func_definition
        content += '\n'
        content += StringUtils.gen_docstring(self.description, 2)
        content += '\n'
        content += self.endpoint_body
        return content


class EndpointCollection:
    entity_path_name = 'entities'
    endpoints_path_name = 'endpoints'
    file_extension = '.py'
    sync_client_name = 'BungieClientSync'
    async_client_name = 'BungieClientAsync'
    sync_client_file_name = 'client_sync'
    async_client_file_name = 'client_async'

    sync_endpoints: list[Endpoint | OAuthEndpoint]
    async_endpoints: list[Endpoint | OAuthEndpoint]

    def __init__(self, name: str, bungie_root: Server, manifest_entities: list[Entity]):
        self.name = name
        self.bungie_root = bungie_root
        self.manifest_entities = manifest_entities
        self.sync_imports = EntityImportCollection([
            EntityImport(
                name=f'.{self.sync_client_file_name}',
                type=ImportType.relative,
                imports=[self.sync_client_name],
                type_check=True,
            ),
        ])
        self.async_imports = EntityImportCollection([
            EntityImport(
                name=f'.{self.async_client_file_name}',
                type=ImportType.relative,
                imports=[self.async_client_name],
                type_check=True,
            ),
        ])
        self.sync_endpoints = []
        self.async_endpoints = []

        if self.name == 'Destiny2':
            self.sync_imports.add_import(EntityImport(
                name=f'.{self.entity_path_name}',
                type=ImportType.relative,
                imports=[e.name_safe for e in self.manifest_entities]
            ))
            self.async_imports.add_import(EntityImport(
                name=f'.{self.entity_path_name}',
                type=ImportType.relative,
                imports=[e.name_safe for e in self.manifest_entities]
            ))

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

    def add_endpoint(self, path: str, endpoint: PathItem, entities: EntityCollection) -> None:
        sync_endpoint = Endpoint(path, endpoint, entities, False)
        self.sync_endpoints.append(sync_endpoint)
        self.sync_imports.add_collection(sync_endpoint.imports)

        async_endpoint = Endpoint(path, endpoint, entities, True)
        self.async_endpoints.append(async_endpoint)
        self.async_imports.add_collection(async_endpoint.imports)

    def add_oauth_endpoint(self, path: str, is_refresh: bool) -> None:
        sync_endpoint = OAuthEndpoint(path, False, is_refresh)
        self.sync_endpoints.append(sync_endpoint)
        self.sync_imports.add_collection(sync_endpoint.imports)

        async_endpoint = OAuthEndpoint(path, True, is_refresh)
        self.async_endpoints.append(async_endpoint)
        self.async_imports.add_collection(async_endpoint.imports)

    def write_files(self, folder: str) -> None:
        with open(os.path.join(folder, self.file_name_sync + self.file_extension), 'w+') as endpoint_file:
            endpoint_file.write(self.text_content_sync)

        with open(os.path.join(folder, self.file_name_async + self.file_extension), 'w+') as endpoint_file:
            endpoint_file.write(self.text_content_async)
