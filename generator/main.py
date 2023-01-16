import json
import os
from typing import Optional

import requests
from alive_progress import alive_bar

from generator.models.client import Client
from .models.endpoints import EndpointCollection
from .models.entity import EntityCollection
from .models.enum_class import EnumCollection
from .utils.str_utils import StringUtils
from .models.entity_import import EntityImport, EntityImportCollection
from .models.enums import ImportType, PropertyType
from .models.openapi.open_api import OpenApi


open_api_spec = "https://raw.githubusercontent.com/Bungie-net/api/master/openapi.json"


class APIGenerator:
    max_line_length = 120
    generated_path = './generated'
    entities_path_name = 'entities'
    endpoints_path_name = 'endpoints'
    utils_path_name = 'utils'
    file_extension = '.py'

    readme_file = 'README.md'
    datetime_utils_file = 'datetime_utils'
    enum_utils_file = 'enum_utils'
    byte_utils_file = 'byte_utils'
    union_field_file = 'union_field'
    oauth_util_file = 'oauth_utils'
    exceptions_file = 'exceptions'
    entity_model_file = 'models'
    enum_model_file = 'enums'
    responses_model_file = 'responses'

    default_entity_imports = EntityImportCollection([
        EntityImport(
            name='dataclasses',
            type=ImportType.stdlib,
            imports=['dataclass', 'field'],
        ),
        EntityImport(
            name='dataclasses_json',
            type=ImportType.external,
            imports=['dataclass_json']
        ),
        EntityImport(
            name='typing',
            type=ImportType.stdlib,
            imports=['Optional']
        )
    ])

    default_entity_decorators = [
        '@dataclass_json',
        '@dataclass(kw_only=True)',
    ]
    indent = '    '

    enums: EnumCollection
    entities: EntityCollection
    responses: EntityCollection
    endpoints: dict[str, EndpointCollection]
    clients: list[Client]

    oauth_url: Optional[str]
    token_url: Optional[str]
    refresh_url: Optional[str]
    oauth_scopes: Optional[dict[str, str]]
    api_key_header: Optional[str]
    api_key_var: Optional[str]

    def __init__(self):
        self.spec = self.load_spec()
        self.enums = EnumCollection()
        self.entities = EntityCollection()
        self.responses = EntityCollection()
        self.endpoints = {}
        self.clients = []

        self.oauth_url = None
        self.token_url = None
        self.refresh_url = None
        self.oauth_scopes = None
        self.api_key_var = None
        self.api_key_header = None

    @staticmethod
    def load_spec() -> OpenApi:
        print('LOADING OPEN API SPEC')
        with requests.get(open_api_spec) as r:
            r.raise_for_status()
            return OpenApi.schema().load(r.json())

    @classmethod
    def process_namespace(cls) -> None:
        # Create package folder
        if not os.path.exists(cls.generated_path):
            os.mkdir(cls.generated_path)

        # Create entities subdir
        entity_base = os.path.join(cls.generated_path, cls.entities_path_name)
        if not os.path.exists(entity_base):
            os.mkdir(entity_base)

        # Create utils subdir
        utils_base = os.path.join(cls.generated_path, cls.utils_path_name)
        if not os.path.exists(utils_base):
            os.mkdir(utils_base)

        # Create endpoints subdir
        endpoints_base = os.path.join(cls.generated_path, cls.endpoints_path_name)
        if not os.path.exists(endpoints_base):
            os.mkdir(endpoints_base)

    def write_init(self) -> None:
        with open(os.path.join(self.generated_path, '__init__.py'), 'w+'):
            pass

        with open(
                os.path.join(
                    self.generated_path,
                    self.entities_path_name,
                    '__init__.py'
                ),
                'w+',
        ) as entity_init:
            content = StringUtils.gen_line_break_comment('ENUM IMPORTS')
            content += '\n'
            content += '\n'.join(self.enums.init_imports)
            content += '\n\n'
            content += StringUtils.gen_line_break_comment('ENTITY IMPORTS')
            content += '\n'
            content += '\n'.join(self.entities.init_imports)
            content += '\n\n'
            content += StringUtils.gen_line_break_comment('RESPONSE IMPORTS')
            content += '\n'
            content += '\n'.join(self.responses.init_imports)
            content += '\n\n'

            entity_init.write(content)

        with open(
            os.path.join(
                self.generated_path,
                self.endpoints_path_name,
                '__init__.py',
            ),
            'w+',
        ) as endpoint_init:
            imports = EntityImportCollection()
            names = []
            for endpoint in self.endpoints.values():
                imports.add_collection(endpoint.init_imports)
                names.append(endpoint.name_sync)
                names.append(endpoint.name_async)
            content = StringUtils.gen_line_break_comment('ENDPOINT IMPORTS')
            content += '\n'
            content += '\n'.join(i.import_string for i in imports.imports_sorted)
            content += '\n\n\n'
            content += '__all__ = ' + json.dumps(
                names,
                indent=2
            )
            content += '\n'

            endpoint_init.write(content)

        with open(os.path.join(self.generated_path, '__init__.py'), 'w+') as client_init:
            names = [c.name for c in self.clients]
            imports = [c.init_string for c in self.clients]

            content = StringUtils.gen_line_break_comment('CLIENT IMPORTS')
            content += '\n'
            content += '\n'.join(imports)
            content += '\n\n\n'
            content += '__all__ = ' + json.dumps(names, indent=2)
            content += '\n'
            client_init.write(content)

    def gen_entities(self) -> None:
        # Ensure that the necessary folders exist.
        self.process_namespace()

        # Process component schemas
        with alive_bar(
                len(self.spec.components.schemas),
                force_tty=True,
                title='SCHEMAS',
                title_length=12
        ) as bar:
            for k, schema in self.spec.components.schemas.items():
                # Handle enums
                if schema.enum:
                    self.enums.add_enum(k, schema)
                elif PropertyType(schema.type) in (PropertyType.object, PropertyType.array):
                    self.entities.add_entity(k, schema)
                else:
                    print(f'UNHANDLED SCHEMA TYPE: {k} - {schema.type} - {schema}')
                bar()

        self.enums.write_enum_file(os.path.join(
            self.generated_path,
            self.entities_path_name,
            self.enum_model_file + self.file_extension
        ))
        self.entities.write_entity_file(os.path.join(
            self.generated_path,
            self.entities_path_name,
            self.entity_model_file + self.file_extension
        ))

    def gen_responses(self) -> None:
        # Ensure that the necessary folders exist.
        self.process_namespace()

        # Process component schemas
        with alive_bar(
                len(self.spec.components.responses),
                force_tty=True,
                title='RESPONSES',
                title_length=12
        ) as bar:
            for k, response in self.spec.components.responses.items():
                if PropertyType(response.content['application/json'].schema.type) in (PropertyType.object, PropertyType.array):
                    self.responses.add_response(k, response)
                else:
                    print(f'UNHANDLED RESPONSE TYPE: {k} - {response.content["application/json"].schema.type} - '
                          f'{response.content["application/json"].schema}')
                bar()

        self.responses.write_entity_file(os.path.join(
            self.generated_path,
            self.entities_path_name,
            self.responses_model_file + self.file_extension
        ))

    def gen_endpoints(self) -> None:
        # Ensure that the necessary folders exist
        self.process_namespace()

        # Process path schemas
        with alive_bar(
                len(self.spec.paths),
                force_tty=True,
                title='ENDPOINTS',
                title_length=12
        ) as bar:
            for path, endpoint in self.spec.paths.items():
                coll_name = endpoint.summary.split('.')[0]
                if not coll_name:
                    coll_name = 'Core'
                if coll_name not in self.endpoints:
                    self.endpoints[coll_name] = EndpointCollection(
                        coll_name,
                        bungie_root=self.spec.servers[0],
                        manifest_entities=self.entities.manifest_entities,
                    )
                self.endpoints[coll_name].add_endpoint(path, endpoint, self.entities)
                bar()

            for name, collection in self.endpoints.items():
                collection.write_files(os.path.join(self.generated_path, self.endpoints_path_name))

    def gen_clients(self) -> None:
        # Ensure that the necessary folders exist
        self.process_namespace()

        # Create client classes for async and async
        with alive_bar(
            2,
            force_tty=True,
            title='CLIENTS',
            title_length=12,
        ) as bar:
            sync_client = Client(
                False,
                self.api_key_var,
                self.api_key_header,
                self.oauth_url,
                list(self.endpoints.values())
            )
            sync_client.write_file(self.generated_path)
            self.clients.append(sync_client)
            bar()

            async_client = Client(
                True,
                self.api_key_var,
                self.api_key_header,
                self.oauth_url,
                list(self.endpoints.values())
            )
            async_client.write_file(self.generated_path)
            self.clients.append(async_client)
            bar()

    def gen_readme(self) -> None:
        readme_count = 1
        with alive_bar(readme_count, title='README FILES', force_tty=True, title_length=12) as bar:
            content = f'# {self.spec.info.title} - {self.spec.info.version}'
            content += '\n\n'
            content += '\n'.join(StringUtils.split_text_for_wrapping(self.spec.info.description))
            content += '\n\n'
            content += f'This content is automatically generated via the OpenAPI {self.spec.openapi} specification ' \
                       f'provided by Bungie.'
            content += '\n\n'
            content += '### Resources'
            content += '\n\n'
            content += f'- [Terms of Service]({self.spec.info.termsOfService})'
            content += '\n'
            content += f'- Contact: [{self.spec.info.contact.name}](mailto:{self.spec.info.contact.email})'
            content += '\n'
            content += f'- Github: {self.spec.info.contact.url}'
            content += '\n'
            content += f'- License: [{self.spec.info.license.name}]({self.spec.info.license.url})'
            content += '\n\n'
            content += '#### External Documentation'
            content += '\n\n'
            content += f'- [{self.spec.externalDocs.description}]({self.spec.externalDocs.url})'

            if not os.path.exists(self.generated_path):
                os.mkdir(self.generated_path)
            with open(os.path.join(self.generated_path, self.readme_file), 'w+') as readme:
                readme.write(content)
            bar()

    def gen_utils(self) -> None:
        util_count = 3
        with alive_bar(util_count, title='UTIL FILES', force_tty=True, title_length=12) as bar:

            # Ensure path and default files exist.
            if not os.path.exists(self.generated_path):
                os.mkdir(self.generated_path)
            if not os.path.exists(os.path.join(self.generated_path, self.utils_path_name)):
                os.mkdir(os.path.join(self.generated_path, self.utils_path_name))
            if not os.path.exists(os.path.join(self.generated_path, self.utils_path_name, '__init__.py')):
                with open(os.path.join(self.generated_path, self.utils_path_name, '__init__.py'), 'w+') as f:
                    f.write('')

            # Union field utils
            with open(
                    os.path.join(self.generated_path, self.utils_path_name, self.union_field_file + self.file_extension),
                    'w+'
            ) as f:
                imports = EntityImportCollection([
                    EntityImport(name='typing', type=ImportType.stdlib, alias='t'),
                    EntityImport(name='marshmallow', type=ImportType.external),
                    EntityImport(name='marshmallow.error_store', type=ImportType.external),
                    EntityImport(name='marshmallow.exceptions', type=ImportType.external)
                ])
                content = imports.formatted_imports
                content += '\n'

                # Exception class
                content += StringUtils.gen_class_declaration('MarshmallowUnionException', ['Exception'])
                content += '\n'
                content += StringUtils.gen_docstring('Base exception for marshmallow_union.', 1)
                content += '\n\n\n'

                # Exception group class
                content += StringUtils.gen_class_declaration('ExceptionGroup', ['MarshmallowUnionException'])
                content += '\n'
                content += StringUtils.gen_docstring('Collection of possibly multiple exceptions.', 1)
                content += '\n\n'
                content += StringUtils.indent_str('def __init__(self, msg: str, errors: list[Exception]) -> None:\n', 1)
                content += StringUtils.indent_str('self.msg = msg\n', 2)
                content += StringUtils.indent_str('self.errors = errors\n', 2)
                content += StringUtils.indent_str('super().__init__(msg, errors)\n', 2)
                content += '\n\n'

                # Union class
                content += StringUtils.gen_class_declaration('UnionField', ['marshmallow.fields.Field'])
                content += '\n'
                content += StringUtils.gen_docstring(
                    'Field that accepts any one of multiple fields. Each argument will be tried until '
                    'one succeeds.', 1
                )
                content += '\n\n'
                content += StringUtils.indent_str('def __init__(\n', 1)
                content += StringUtils.indent_str('self,\n', 2)
                content += StringUtils.indent_str('fields: t.List[marshmallow.fields.Field],\n', 2)
                content += StringUtils.indent_str('reverse_serialize_candidates: bool = False,\n', 2)
                content += StringUtils.indent_str('**kwargs\n', 2)
                content += StringUtils.indent_str('):\n', 1)
                content += StringUtils.indent_str('self._candidate_fields = fields\n', 2)
                content += StringUtils.indent_str('self._reverse_serialize_candidates = reverse_serialize_candidates\n', 2)
                content += StringUtils.indent_str('super().__init__(**kwargs)\n', 2)
                content += '\n'
                content += StringUtils.indent_str('def _serialize(self, value: t.Any, attr: str, obj: str, **kwargs):\n', 1)
                content += StringUtils.gen_docstring(
                    'Pulls the value for the given key from the object, applies the '
                    'field\'s formatting and returns the result.',
                    2
                )
                content += '\n\n'
                content += StringUtils.indent_str(
                    'error_store = kwargs.pop("error_store", marshmallow.error_store.ErrorStore())\n',
                    2,
                )
                content += StringUtils.indent_str('fields = self._candidate_fields\n', 2)
                content += StringUtils.indent_str('if self._reverse_serialize_candidates:\n', 2)
                content += StringUtils.indent_str('fields = list(reversed(fields))\n', 3)
                content += '\n'
                content += StringUtils.indent_str('for candidate_field in fields:\n', 2)
                content += StringUtils.indent_str('try:\n', 3)
                content += StringUtils.indent_str('return candidate_field._serialize(\n', 4)
                content += StringUtils.indent_str('value, attr, obj, error_store=error_store, **kwargs\n', 5)
                content += StringUtils.indent_str(')\n', 4)
                content += StringUtils.indent_str('except (TypeError, ValueError) as e:\n', 3)
                content += StringUtils.indent_str('error_store.store_error({attr: e})\n', 4)
                content += '\n'
                content += StringUtils.indent_str(
                    'raise ExceptionGroup("All serializers raised exceptions.\\n", error_store.errors)\n',
                    2,
                )
                content += '\n'
                content += StringUtils.indent_str('def _deserialize(self, value, attr=None, data=None, **kwargs):\n', 1)
                content += StringUtils.gen_docstring('Deserializes ``value``.', 2)
                content += '\n\n'
                content += StringUtils.indent_str('errors = []\n', 2)
                content += StringUtils.indent_str('for candidate_field in self._candidate_fields:\n', 2)
                content += StringUtils.indent_str('try:\n', 3)
                content += StringUtils.indent_str('return candidate_field.deserialize(value, attr, data, **kwargs)\n', 4)
                content += StringUtils.indent_str('except marshmallow.exceptions.ValidationError as exc:\n', 3)
                content += StringUtils.indent_str('errors.append(exc.messages)\n', 4)
                content += StringUtils.indent_str(
                    'raise marshmallow.exceptions.ValidationError(message=errors, field_name=attr)\n',
                    2
                )

                f.write(content)
            bar()

            with open(
                os.path.join(self.generated_path, self.utils_path_name, self.oauth_util_file + self.file_extension),
                'w+'
            ) as f:
                imports = EntityImportCollection([
                    EntityImport(name='datetime', type=ImportType.stdlib, imports=['datetime', 'timedelta']),
                    EntityImport(name='dataclasses', type=ImportType.stdlib, imports=['dataclass', 'field']),
                    EntityImport(name='dataclasses_json', type=ImportType.external, imports=['dataclass_json']),
                    EntityImport(name='typing', type=ImportType.stdlib, imports=['Optional']),
                    EntityImport(name='enum', type=ImportType.stdlib, imports=['Enum']),
                ])

                content = imports.formatted_imports
                content += '\n'

                content += StringUtils.gen_class_declaration('OAuthException', ['Exception'])
                content += '\n'
                content += StringUtils.indent_str('pass\n', 1)
                content += '\n\n'
                content += StringUtils.gen_class_declaration('OAuthInformationNotProvided', ['OAuthException'])
                content += '\n'
                content += StringUtils.indent_str('pass\n', 1)
                content += '\n\n'
                content += StringUtils.gen_class_declaration('OAuthContextExpired', ['OAuthException'])
                content += '\n'
                content += StringUtils.indent_str('pass\n', 1)
                content += '\n\n'
                content += StringUtils.gen_class_declaration('OAuthContextNotFound', ['OAuthException'])
                content += '\n'
                content += StringUtils.indent_str('pass\n', 1)
                content += '\n\n'
                content += StringUtils.gen_class_declaration('OAuthInitFailure', ['OAuthException'])
                content += '\n'
                content += StringUtils.indent_str('pass\n', 1)
                content += '\n\n'

                content += StringUtils.gen_class_declaration('OAuthClientType', ['Enum'])
                content += '\n'
                content += StringUtils.indent_str('NotApplicable = 0\n', 1)
                content += StringUtils.indent_str('Public = 1\n', 1)
                content += StringUtils.indent_str('Confidential = 2\n', 1)
                content += '\n\n'

                content += '@dataclass_json\n'
                content += '@dataclass(kw_only=True)\n'
                content += StringUtils.gen_class_declaration('AccessToken')
                content += '\n'
                content += StringUtils.gen_comment('Standard Bungie fields.', 1)
                content += '\n'
                content += StringUtils.indent_str('access_token: str\n', 1)
                content += StringUtils.indent_str('token_type: str\n', 1)
                content += StringUtils.indent_str('expires_in: int\n', 1)
                content += '\n'
                content += StringUtils.gen_comment('Public OAuth applications do not include refresh information.', 1)
                content += '\n'
                content += StringUtils.indent_str('refresh_token: Optional[str] = field(default=None)\n', 1)
                content += StringUtils.indent_str('refresh_expires_in: Optional[int] = field(default=None)\n', 1)
                content += StringUtils.indent_str('membership_id: Optional[int] = field(default=None)\n', 1)
                content += '\n'
                content += StringUtils.gen_comment('Customer helper fields.', 1)
                content += '\n'
                content += StringUtils.indent_str('expires_at: Optional[datetime] = field(default=None)\n', 1)
                content += StringUtils.indent_str('refresh_expires_at: Optional[datetime] = field(default=None)\n', 1)
                content += '\n'
                content += StringUtils.gen_function_declaration('__post_init__', ['self'], depth=1)
                content += '\n'
                content += StringUtils.indent_str('self.expires_in -= 5\n', 2)
                content += StringUtils.indent_str('if self.refresh_expires_in:\n', 2)
                content += StringUtils.indent_str('self.refresh_expires_in -= 5\n', 3)
                content += StringUtils.indent_str(
                    'self.expires_at = datetime.utcnow() + timedelta(seconds=self.expires_in)\n',
                    2
                )
                content += StringUtils.indent_str('if self.refresh_expires_in:\n', 2)
                content += StringUtils.indent_str(
                    'self.refresh_expires_at = datetime.utcnow() + timedelta(seconds=self.refresh_expires_in)\n',
                    3
                )
                content += '\n'

                content += StringUtils.indent_str('@property\n', 1)
                content += StringUtils.gen_function_declaration(
                    'header',
                    ['self'],
                    'str',
                    depth=1,
                )
                content += '\n'
                content += StringUtils.indent_str(
                    'return f\'{self.token_type} {self.access_token}\'\n',
                    2
                )
                content += '\n'

                content += StringUtils.indent_str('@property\n', 1)
                content += StringUtils.gen_function_declaration(
                    'is_expired',
                    ['self'],
                    'bool',
                    depth=1,
                )
                content += '\n'
                content += StringUtils.indent_str('if self.expires_at:\n', 2)
                content += StringUtils.indent_str('return datetime.utcnow() >= self.expires_at\n', 3)
                content += StringUtils.indent_str('else:\n', 2)
                content += StringUtils.indent_str('return True\n', 3)
                content += '\n'

                content += StringUtils.indent_str('@property\n', 1)
                content += StringUtils.gen_function_declaration(
                    'is_refresh_expired',
                    ['self'],
                    'bool',
                    depth=1,
                )
                content += '\n'
                content += StringUtils.indent_str('if self.refresh_expires_at:\n', 2)
                content += StringUtils.indent_str('return datetime.utcnow() >= self.refresh_expires_at\n', 3)
                content += StringUtils.indent_str('else:\n', 2)
                content += StringUtils.indent_str('return True\n', 3)

                f.write(content)
            bar()

            with open(
                os.path.join(self.generated_path, self.utils_path_name, self.exceptions_file + self.file_extension),
                'w+'
            ) as f:
                imports = EntityImportCollection([EntityImport(
                    name=f'.{self.entities_path_name}',
                    type=ImportType.relative,
                    imports=['PlatformErrorCodes'],
                )])
                content = imports.formatted_imports
                content += '\n'

                content += StringUtils.gen_class_declaration('BungieApiError', ['BaseException'])
                content += '\n'
                content += StringUtils.gen_function_declaration('__init__', [
                    'self',
                    'method: str',
                    'url: str',
                    'status_code: int',
                    'error_code: PlatformErrorCodes',
                    'message: str',
                ], depth=1)
                content += '\n'
                content += StringUtils.indent_str(
                    'super().__init__(f\'[{method.upper()} {status_code} {url}]\\n'
                    '\\t{error_code.value} {error_code.name} - {message}\')\n',
                    2
                )

                f.write(content)
            bar()

    def gen_security(self) -> None:
        with alive_bar(
            len(self.spec.components.securitySchemes),
            title='SECURITY',
            force_tty=True,
            title_length=12,
        ) as bar:
            for name, scheme in self.spec.components.securitySchemes.items():
                if name == 'oauth2':
                    self.oauth_url = scheme.flows.authorizationCode.authorizationUrl
                    self.token_url = scheme.flows.authorizationCode.tokenUrl
                    self.refresh_url = scheme.flows.authorizationCode.refreshUrl
                    self.oauth_scopes = scheme.flows.authorizationCode.scopes

                    collection = EndpointCollection(
                        'Oauth',
                        bungie_root=self.spec.servers[0],
                        manifest_entities=self.entities.manifest_entities,
                    )
                    collection.add_oauth_endpoint(self.token_url, False)
                    collection.add_oauth_endpoint(self.refresh_url, True)
                    collection.write_files(os.path.join(self.generated_path, self.endpoints_path_name))
                    self.endpoints['Oauth'] = collection
                elif name == 'apiKey' and scheme.in_ == 'header':
                    self.api_key_header = scheme.name
                    self.api_key_var = StringUtils.camel_to_snake(scheme.type)
                else:
                    print(f'UNHANDLED SECURITY SCHEME: {name} - {scheme}')
                bar()

    def gen(self) -> None:
        self.process_namespace()

        self.gen_entities()
        self.gen_readme()
        self.gen_utils()
        self.gen_responses()
        self.gen_endpoints()
        self.gen_security()
        self.gen_clients()
        self.write_init()


if __name__ == "__main__":
    generator = APIGenerator()
    # generator.gen_entities()
    # generator.gen_readme()
    # generator.gen_utils()
