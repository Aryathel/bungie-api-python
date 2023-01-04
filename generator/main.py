import os

import requests

from .utils.str_utils import StringUtils
from .models.class_property import ClassProperty
from .models.entity_import import EntityImport, EntityImportCollection
from .models.enums import ImportType, PropertyType, PropertyFormat
from .models.open_api.open_api_schema import OpenAPISchema
from .models.open_api.open_api_spec import OpenAPISpec


open_api_spec = "https://raw.githubusercontent.com/Bungie-net/api/master/openapi-2.json"


class APIGenerator:
    registry: dict[str, dict[str, str]]

    max_line_length = 120
    generated_path = './generated'
    entities_path_name = 'entities'
    utils_path_name = 'utils'
    file_extension = '.py'

    readme_file = 'README.md'
    datetime_utils_file = 'datetime_utils'
    enum_utils_file = 'enum_utils'

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

    def __init__(self):
        self.spec = self.load_spec()

    @staticmethod
    def load_spec() -> OpenAPISpec:
        with requests.get(open_api_spec) as r:
            r.raise_for_status()
            return OpenAPISpec.from_dict(r.json())

    @staticmethod
    def gen_import(pkg: str, imp: list[str] = None, relative: bool = False) -> str:
        if relative:
            pkg = f'.{pkg}'

        if imp:
            return f'from {pkg} import {", ".join(imp)}'
        else:
            return f'import {pkg}'

    @classmethod
    def entity_decorators(cls, decorators: list[str] = None, depth: int = 0) -> str:
        if decorators:
            return '\n'.join(f'{cls.indent * depth}{l}' for l in cls.default_entity_decorators + decorators)
        else:
            return '\n'.join(f'{cls.indent * depth}{l}' for l in cls.default_entity_decorators)

    @classmethod
    def gen_import_from_ref(cls, path: str, ref: str) -> tuple[EntityImport, str]:
        depth = path.count('.')
        cur = path.split('.')[-1]
        ref = ref.split('/')[-1]
        name = ref
        split = name.split('.')
        path = '.'.join(StringUtils.camel_to_snake(i) for i in split)
        cls_name = split[-1]

        imp = EntityImport(
            name=f'{"."*depth}{path}',
            type=ImportType.relative,
            imports=[cls_name],
            self_ref=cls_name == cur,
        )

        if cls_name == cur:
            cls_name = f'\'{cls_name}\''

        return imp, cls_name

    @classmethod
    def process_namespace(cls, path: str) -> tuple[str, str]:
        if '.' in path:
            key = [StringUtils.camel_to_snake(n) for n in path.split('.')]
        else:
            key = StringUtils.camel_to_snake(path)

        entity_base = os.path.join(cls.generated_path, cls.entities_path_name)
        if not os.path.exists(cls.generated_path):
            os.mkdir(cls.generated_path)
        if not os.path.exists(os.path.join(cls.generated_path, '__init__.py')):
            with open(os.path.join(cls.generated_path, '__init__.py'), 'w+') as init:
                init.write('')
        if not os.path.exists(entity_base):
            os.mkdir(entity_base)
        if not os.path.exists(os.path.join(entity_base, '__init__.py')):
            with open(os.path.join(entity_base, '__init__.py'), 'w+') as init:
                init.write('')

        if isinstance(key, list):
            for p in key[:-1]:
                entity_base = os.path.join(entity_base, p)
                if not os.path.exists(entity_base):
                    os.mkdir(entity_base)
                if not os.path.exists(os.path.join(entity_base, '__init__.py')):
                    with open(os.path.join(entity_base, '__init__.py'), 'w+') as init:
                        init.write('')
            file = os.path.join(entity_base, key[-1]) + cls.file_extension
        else:
            file = os.path.join(entity_base, key) + cls.file_extension

        return file, path.split('.')[-1]

    @staticmethod
    def class_declaration(class_name: str, inheritance: list[str] | str = None) -> str:
        if not inheritance:
            return f'class {class_name}:'
        else:
            if isinstance(inheritance, str):
                return f'class {class_name}({inheritance}):'
            else:
                return f'class {class_name}({", ".join(inheritance)}:'

    @classmethod
    def generate_model_properties(
            cls,
            path: str,
            entity: OpenAPISchema
    ) -> tuple[EntityImportCollection, list[ClassProperty]]:
        imports = EntityImportCollection()
        properties = []
        if entity.properties:
            for k, prop in entity.properties.items():
                prop_type = PropertyType(prop.type)
                fmt = PropertyFormat(prop.format)

                if prop_type == PropertyType.array:
                    if prop.items.is_ref:
                        array_item_type = prop.items.ref
                        imp, ref_name = cls.gen_import_from_ref(path, array_item_type)
                        imports.add_import(imp)
                        properties.append(ClassProperty(
                            name=k,
                            type=ref_name,
                            optional=True,
                            list=True,
                            comment=prop.description,
                        ))
                    elif prop.items.is_enum_reference:
                        imp, cls_name = cls.gen_import_from_ref(path, prop.items.x_enum_reference.ref)
                        imports.add_import(imp)
                        properties.append(ClassProperty(
                            name=k,
                            type=cls_name,
                            optional=True,
                            comment=prop.description,
                            list=True,
                        ))
                    else:
                        print(f'UNHANDLED ARRAY PROPERTY: {path} - {k} - {prop}')
                elif prop_type == PropertyType.string:
                    if fmt == PropertyFormat.datetime:
                        imports.add_import(EntityImport(
                            name='datetime',
                            type=ImportType.stdlib,
                            imports=['datetime']
                        ))
                        imports.add_import(EntityImport(
                            name=f'{"."*(path.count(".")+1)}{cls.utils_path_name}.{cls.datetime_utils_file}',
                            type=ImportType.relative,
                            imports=['DATETIME_META']
                        ))
                        properties.append(ClassProperty(
                            name=k,
                            type='datetime',
                            optional=True,
                            comment=prop.description,
                        ))
                    elif fmt == PropertyFormat.none:
                        properties.append(ClassProperty(
                            name=k,
                            type='str',
                            optional=True,
                            comment=prop.description,
                        ))
                    else:
                        print(f'UNHANDLED STRING FORMAT: {path} - {k} - {prop}')
                elif prop_type == PropertyType.number:
                    if fmt == PropertyFormat.double:
                        properties.append(ClassProperty(
                            name=k,
                            type='float',
                            optional=True,
                            comment=prop.description,
                        ))
                elif prop_type == PropertyType.integer:
                    if not prop.is_enum_reference:
                        properties.append(ClassProperty(
                            name=k,
                            type='int',
                            optional=True,
                            comment=prop.description,
                        ))
                    else:
                        imp, cls_name = cls.gen_import_from_ref(path, prop.x_enum_reference.ref)
                        imports.add_import(imp)
                        imports.add_import(EntityImport(
                            name=f'{"."*(path.count(".")+1)}{cls.utils_path_name}.{cls.enum_utils_file}',
                            type=ImportType.relative,
                            imports=['ENUM_META']
                        ))
                        properties.append(ClassProperty(
                            name=k,
                            type=cls_name,
                            optional=True,
                            comment=prop.description,
                            is_enum=True
                        ))
                elif prop_type == PropertyType.boolean:
                    properties.append(ClassProperty(
                        name=k,
                        type='bool',
                        optional=True,
                        comment=prop.description,
                    ))
                elif prop_type == PropertyType.object:
                    if prop.additionalProperties and prop.additionalProperties.is_ref:
                        imp, cls_name = cls.gen_import_from_ref(path, prop.additionalProperties.ref)
                        imports.add_import(imp)
                        properties.append(ClassProperty(
                            name=k,
                            type=cls_name,
                            optional=True,
                            comment=prop.description,
                        ))
                    elif prop.additionalProperties and prop.additionalProperties.type == PropertyType.string.value:
                        properties.append(ClassProperty(
                            name=k,
                            type='dict[str, str]',
                            optional=True,
                            comment=prop.description,
                        ))
                    else:
                        print(f'UNHANDLED OBJECT PROPERTY TYPE: {path} - {k} - {prop}')
                elif prop.is_ref:
                    imp, cls_name = cls.gen_import_from_ref(path, prop.ref)
                    imports.add_import(imp)
                    properties.append(ClassProperty(
                        name=k,
                        type=cls_name,
                        optional=True,
                        comment=prop.description,
                    ))
                else:
                    print(f'UNHANDLED PROPERTY TYPE: {path} - {k} - {prop_type}')
        else:
            print(f'ENTITY HAS NO PROPERTIES: {path}')

        return imports, properties

    @classmethod
    def generate_class(cls, file: str, class_name: str, qualified_class_name: str, entity: OpenAPISchema) -> None:
        default_imports = cls.default_entity_imports.copy()

        imports, properties = cls.generate_model_properties(qualified_class_name, entity)

        default_imports.add_collection(imports)

        # Handle necessary imports
        body = [default_imports.formatted_imports]

        body.append(StringUtils.gen_line_break_comment('MODEL DEFINITION'))

        # Handle the class decorators
        body.append(cls.entity_decorators())

        # Attach the class declaration
        body.append(cls.class_declaration(class_name))

        # Handle the class description as a docstring
        if entity.description:
            body.append(StringUtils.gen_docstring(entity.description, depth=1))

        # Attach the class body.
        # TODO: Implement the actual class body.
        if not properties:
            body.append(cls.indent + 'pass')
        else:
            body.append('\n'.join(f'{p.field_definition}' for p in properties))

        # Line break at the end of the file.
        body.append('')

        with open(file, 'w+') as class_file:
            class_file.write('\n'.join(body))

    @classmethod
    def generate_enum(cls, file: str, class_name: str, entity: OpenAPISchema) -> None:
        pass

    def gen_entities(self) -> None:
        self.registry = {}

        # Ensure that the necessary folders exist.
        count = 2000
        for k, entity in self.spec.definitions.items():
            if count == 0:
                break
            file, class_name = self.process_namespace(k)
            self.registry[k] = {
                'file': file,
                'class': class_name,
            }
            count -= 1

        # Generate the entity classes.
        count = 2000
        for k, entity in self.spec.definitions.items():
            if count == 0:
                break
            if entity.is_object:
                self.generate_class(
                    self.registry[k]['file'],
                    self.registry[k]['class'],
                    k,
                    entity
                )
            elif entity.is_enum:
                self.generate_enum(
                    self.registry[k]['file'],
                    self.registry[k]['class'],
                    entity
                )
            else:
                print(f'UNHANDLED ENTITY: {k}')
            count -= 1

    def gen_readme(self) -> None:
        content = f'# {self.spec.info.title} - {self.spec.info.version}'
        content += '\n\n'
        content += '\n'.join(StringUtils.split_text_for_wrapping(self.spec.info.description))
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

        if not os.path.exists(self.generated_path):
            os.mkdir(self.generated_path)
        with open(os.path.join(self.generated_path, self.readme_file), 'w+') as readme:
            readme.write(content)

    def gen_utils(self) -> None:
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
            content += StringUtils.indent_str("return datetime.fromisoformat(st_str.upper().strip('Z').split('.')[0])\n", 2)
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


if __name__ == "__main__":
    generator = APIGenerator()
    generator.gen_entities()
    generator.gen_readme()
    generator.gen_utils()
