import json
import os

import requests
from alive_progress import alive_bar

from generator.models.openapi.schema import Schema
from .models.entity import Entity, EntityCollection
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
    utils_path_name = 'utils'
    file_extension = '.py'

    readme_file = 'README.md'
    datetime_utils_file = 'datetime_utils'
    enum_utils_file = 'enum_utils'
    byte_utils_file = 'byte_utils'
    union_field_file = 'union_field'
    entity_model_file = 'models'
    enum_model_file = 'enums'

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

    def __init__(self):
        self.spec = self.load_spec()
        self.enums = EnumCollection()
        self.entities = EntityCollection()

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

    def generate_class(self, class_name: str, qualified_class_name: str, entity: Schema) -> None:
        entity_model = Entity(class_name, qualified_class_name, entity)
        self.major_imports.add_collection(entity_model.imports)
        self.entities.append(entity_model)

    def write_objects(self) -> None:
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

    def write_init(self) -> None:
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
            content += '__all__ = ' + json.dumps(self.enums.enum_names + self.entities.entity_names, indent=2)
            content += '\n'
            entity_init.write(content)

    def gen_entities(self) -> None:
        # Ensure that the necessary folders exist.
        self.process_namespace()

        # Process component schemas
        with alive_bar(
                len(self.spec.components.schemas),
                force_tty=True,
                title='LOADING SCHEMA COMPONENTS'
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

        self.write_objects()

    def gen_readme(self) -> None:
        readme_count = 1
        with alive_bar(readme_count, title='GENERATING README FILES', force_tty=True) as bar:
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
        with alive_bar(util_count, title='GENERATING UTIL FILES', force_tty=True) as bar:

            # Ensure path and default files exist.
            if not os.path.exists(self.generated_path):
                os.mkdir(self.generated_path)
            if not os.path.exists(os.path.join(self.generated_path, self.utils_path_name)):
                os.mkdir(os.path.join(self.generated_path, self.utils_path_name))
            if not os.path.exists(os.path.join(self.generated_path, self.utils_path_name, '__init__.py')):
                with open(os.path.join(self.generated_path, self.utils_path_name, '__init__.py'), 'w+') as f:
                    f.write('')

            # Write datetime utils
            with open(
                    os.path.join(self.generated_path, self.utils_path_name, self.datetime_utils_file + self.file_extension),
                    'w+'
            ) as f:
                # String Util Imports
                imports = EntityImportCollection([
                    EntityImport(name='datetime', type=ImportType.stdlib, imports=['datetime']),
                    EntityImport(name='dataclasses_json', type=ImportType.external, imports=['config']),
                    EntityImport(name='marshmallow', type=ImportType.external, imports=['fields'])
                ])

                content = imports.formatted_imports

                # Datetime decoder from string
                content += '\ndef datetime_field_decoder(st_str: str) -> datetime:\n'
                content += StringUtils.indent_str('if st_str:\n', 1)
                content += StringUtils.indent_str(
                    "return datetime.fromisoformat(st_str.upper().strip('Z').split('.')[0])\n",
                    2
                )
                content += '\n\n'

                # Datetime encoder to string
                content += 'def datetime_field_encoder(dt: datetime) -> str:\n'
                content += StringUtils.indent_str('if dt:\n', 1)
                content += StringUtils.indent_str("return dt.isoformat() + '.00Z'\n", 2)
                content += '\n\n'

                # Datetime metadata
                content += 'DATETIME_META = config(\n'
                content += StringUtils.indent_str('encoder=datetime_field_encoder,\n', 1)
                content += StringUtils.indent_str('decoder=datetime_field_decoder,\n', 1)
                content += StringUtils.indent_str('mm_field=fields.DateTime(format=\'iso\')\n', 1)
                content += ')\n\n'

                f.write(content)
            bar()

            with open(
                    os.path.join(self.generated_path, self.utils_path_name, self.enum_utils_file + self.file_extension),
                    'w+'
            ) as f:
                # Enum util imports
                imports = EntityImportCollection([
                    EntityImport(name='enum', type=ImportType.stdlib, imports=['Enum']),
                    EntityImport(name='typing', type=ImportType.stdlib, imports=['Any']),
                    EntityImport(name='dataclasses_json', type=ImportType.external, imports=['config'])
                ])

                content = imports.formatted_imports
                content += '\n'

                # Enum encoder
                content += 'def enum_encoder(enm: Enum) -> Any:\n'
                content += StringUtils.indent_str('return enm.value\n', 1)
                content += '\n\n'

                # Enum metadata
                content += 'ENUM_META = config(encoder=enum_encoder)\n'

                f.write(content)
            bar()

            with open(
                    os.path.join(self.generated_path, self.utils_path_name, self.union_field_file + self.file_extension),
                    'w+'
            ) as f:
                # Byte util imports
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

    def gen(self) -> None:
        self.gen_readme()
        self.gen_utils()
        self.gen_entities()
        self.write_init()


if __name__ == "__main__":
    generator = APIGenerator()
    # generator.gen_entities()
    # generator.gen_readme()
    # generator.gen_utils()
