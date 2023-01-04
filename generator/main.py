import os
import re

import requests

from generator.models.enums import ImportType, PropertyType
from generator.models.open_api.open_api_schema import OpenAPISchema
from generator.models.open_api.open_api_spec import OpenAPISpec


ImportD = dict[str, ImportType | list[str]]
ImportT = dict[str, dict[str, ImportD]]

open_api_spec = "https://raw.githubusercontent.com/Bungie-net/api/master/openapi-2.json"


class APIGenerator:
    registry: dict[str, dict[str, str]]

    max_line_length = 120
    generated_path = './generated'
    entities_path_name = 'entities'
    file_extension = '.py'

    default_entity_imports: ImportT = {
        'dataclasses': {
            'type': ImportType.stdlib,
            'imports': ['dataclass'],
        },
        'dataclasses_json': {
            'type': ImportType.external,
            'imports': ['dataclass_json'],
        },
    }
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
    def camel_to_snake(inp: str) -> str:
        tmp = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', inp)
        tmp2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', tmp).lower()
        return tmp2

    @classmethod
    def split_text_for_wrapping(cls, inp: str, prefix_length: int = 0) -> list[str]:
        lines = []
        inp = inp.split('\n')
        for line in inp:
            if len(line) + prefix_length > cls.max_line_length:
                rind = line.rindex(' ')
                while rind + prefix_length > cls.max_line_length:
                    rind = line.rindex(' ', 0, rind)
                lines.append(line[:rind])
                lines += cls.split_text_for_wrapping(line[rind+1:], prefix_length)
            else:
                lines.append(line)
        return lines

    @classmethod
    def gen_comment(cls, inp: str, depth: int = 0) -> str:
        comment = ''
        for line in cls.split_text_for_wrapping(inp, len(f'{cls.indent*depth}# ')):
            if comment:
                comment += '\n'
            comment += f'{cls.indent*depth}# {line}'
        return comment

    @classmethod
    def gen_docstring(cls, body: str, depth: int = 0) -> str:
        comment = f'{cls.indent * depth}"""'
        for line in cls.split_text_for_wrapping(body, len(cls.indent * depth)):
            if comment:
                comment += '\n'
            comment += f'{cls.indent * depth}{line}'
        comment += f'\n{cls.indent*depth}"""'
        return comment

    @classmethod
    def gen_line_break_comment(cls, inp: str, depth: int = 0) -> str:
        prefix = f'{cls.indent * depth}# --- '
        return f'{prefix}{inp + " ":-<{cls.max_line_length - len(prefix)}}'

    @staticmethod
    def gen_import(pkg: str, imp: list[str] = None, relative: bool = False, depth: int = 0) -> str:
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
    def entity_imports(cls, imp_collection: ImportT = None) -> str:
        imports = {}

        for package, imp in cls.default_entity_imports.items():
            if not imp['type'] in imports:
                imports[imp['type']] = []
            imp_str = cls.gen_import(
                package,
                imp['imports'] if 'imports' in imp else None,
                imp['type'] == ImportType.internal
            )
            imports[imp['type']].append(imp_str)

        if imp_collection:
            for package, imp in imp_collection.items():
                if not imp['type'] in imports:
                    imports[imp['type']] = []
                imp_str = cls.gen_import(
                    package,
                    imp['imports'] if 'imports' in imp else None,
                    imp['type'] == ImportType.internal
                )
                imports[imp['type']].append(imp_str)

        output = ""
        if ImportType.stdlib in imports:
            output += cls.gen_line_break_comment("STANDARD LIBRARY IMPORTS")
            output += '\n'
            output += '\n'.join(imports[ImportType.stdlib])
            output += '\n\n'
        if ImportType.external in imports:
            output += cls.gen_line_break_comment("3RD PARTY LIBRARY IMPORTS")
            output += '\n'
            output += '\n'.join(imports[ImportType.external])
            output += '\n\n'
        if ImportType.internal in imports:
            output += cls.gen_line_break_comment("LOCAL LIBRARY IMPORTS")
            output += '\n'
            output += '\n'.join(imports[ImportType.internal])
            output += '\n\n'
        if ImportType.relative in imports:
            output += cls.gen_line_break_comment("INTERNAL LIBRARY IMPORTS")
            output += '\n'
            output += '\n'.join(imports[ImportType.relative])
            output += '\n\n'

        return output

    @classmethod
    def gen_import_from_ref(cls, ref: str) -> ImportD:
        ref = ref.split('/')[1:]

        if ref[0] == 'definitions':
            name = ref[1]
            split = name.split('.')
            path = '.'.join(cls.camel_to_snake(i) for i in split)
            cls_name = split[-1]
            imports = {
                'type': ImportType.internal,
                'imports': [cls_name],
                'path': f'entities.{path}'
            }

            return imports

    @classmethod
    def process_namespace(cls, path: str) -> tuple[str, str]:
        if '.' in path:
            key = [cls.camel_to_snake(n) for n in path.split('.')]
        else:
            key = cls.camel_to_snake(path)

        entity_base = os.path.join(cls.generated_path, cls.entities_path_name)
        if not os.path.exists(cls.generated_path):
            os.mkdir(cls.generated_path)
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
    def generate_model_properties(cls, entity: OpenAPISchema) -> tuple[ImportT]:
        imports = {}
        for k, prop in entity.properties.items():
            prop_type = PropertyType(prop.type)

            if prop_type == PropertyType.array:
                if prop.items.is_ref:
                    array_item_type = prop.items.ref
                    imp = cls.gen_import_from_ref(array_item_type)
                    if not imp['path'] in imports:
                        imports[imp['path']] = {
                            'type': imp['type'],
                            'imports': imp['imports']
                        }
                    else:
                        for i in imp['imports']:
                            if i not in imports[imp['path']]['imports']:
                                imports[imp['path']]['imports'].append(imp['imports'])
                    print(k, prop_type, array_item_type, imp)
                elif prop.items.is_enum:
                    pass

        return imports,

    @classmethod
    def generate_class(cls, file: str, class_name: str, entity: OpenAPISchema) -> None:
        imports, = cls.generate_model_properties(entity)

        # Handle necessary imports
        body = [cls.entity_imports(imports)]

        # Handle the class decorators
        body.append(cls.entity_decorators())

        # Attach the class declaration
        body.append(cls.class_declaration(class_name))

        # Handle the class description as a docstring
        if entity.description:
            body.append(cls.gen_docstring(entity.description, depth=1))

        # Attach the class body.
        # TODO: Implement the actual class body.
        body.append(cls.indent + 'pass')

        # Line break at the end of the file.
        body.append('')

        with open(file, 'w+') as class_file:
            class_file.write('\n'.join(body))

    @classmethod
    def generate_enum(cls, file: str, class_name: str, entity: OpenAPISchema) -> None:
        pass

    def gen_entities(self) -> None:
        self.registry = {}

        count = 2
        for k, entity in self.spec.definitions.items():
            if count == 0:
                break
            file, class_name = self.process_namespace(k)
            print(
                f'NAMESPACE PROCESSED:',
                f'  TYPE: {"Enum" if entity.is_enum else "Model"}',
                f'  NAME: {k}',
                f'  FILE: {file}',
                sep='\n'
            )
            self.registry[k] = {
                'file': file,
                'class': class_name,
            }
            count -= 1

        count = 2
        for k, entity in self.spec.definitions.items():
            if count == 0:
                break
            if not entity.is_enum:
                self.generate_class(
                    self.registry[k]['file'],
                    self.registry[k]['class'],
                    entity
                )
            else:
                self.generate_enum(
                    self.registry[k]['file'],
                    self.registry[k]['class'],
                    entity
                )
            count -= 1


if __name__ == "__main__":
    generator = APIGenerator()
    generator.gen_entities()
