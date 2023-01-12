from .enums import ImportType, PropertyType, PropertyFormat
from .openapi.reference import Reference
from .openapi.response import Response
from .openapi.schema import Schema
from ..models.class_property import ClassProperty
from ..models.entity_import import EntityImportCollection, EntityImport
from ..utils.str_utils import StringUtils


class Entity:
    file_extension = '.py'
    entities_file_name = 'models'
    enum_file_name = 'enums'
    utils_path_name = 'utils'
    datetime_utils_path_name = 'datetime_utils'
    union_field_path_name = 'union_field'
    default_entity_decorators = [
        '@dataclass_json',
        '@dataclass(kw_only=True)',
    ]
    default_entity_decorators_with_extra = [
        '@dataclass_json(undefined=Undefined.INCLUDE)',
        '@dataclass(kw_only=True)',
    ]

    imports: EntityImportCollection
    properties: list[ClassProperty]

    def __init__(self, qualified_name: str, schema: Schema, allow_extra: bool = False) -> None:
        self.qualified_name = qualified_name
        self.schema = schema
        self.allow_extra = allow_extra

        self.properties = []
        self.imports = EntityImportCollection([
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

        if self.allow_extra:
            self.imports.add_import(EntityImport(
                name='dataclasses_json',
                type=ImportType.external,
                imports=['Undefined', 'CatchAll'],
            ))
            self.properties.append(ClassProperty(
                name='extra_unknown_fields',
                type='CatchAll',
            ))

        self.generate_properties()

    @property
    def name(self) -> str:
        return self.qualified_name.split('.')[-1]

    @property
    def name_safe(self) -> str:
        return self.name.replace('[]', 'Array')

    @property
    def description(self) -> str | None:
        return self.schema.description

    @property
    def is_placeholder(self) -> bool:
        if PropertyType(self.schema.type) == PropertyType.object:
            if not self.schema.properties:
                return True
        return False

    @property
    def is_enum_array_placeholder(self) -> bool:
        if PropertyType(self.schema.type) == PropertyType.array:
            if self.schema.items:
                if self.schema.items.x_enum_reference:
                    return True
        return False

    @property
    def init_import(self) -> str:
        return EntityImport(
            name=self.entities_file_name,
            type=ImportType.relative,
            imports=[self.name_safe],
        ).import_string

    @property
    def formatted_entity(self) -> tuple[str, str]:
        body = []
        # Placeholder type - These have to go at the end of the file to prevent issues
        # with forward references in placeholder types.
        placeholders = []
        if self.is_placeholder:
            placeholders.append(StringUtils.gen_line_break_comment(self.qualified_name))
            if self.description:
                placeholders.append(StringUtils.gen_comment(self.description))

            if self.schema.additionalProperties and self.schema.additionalProperties.ref:
                cls_name = StringUtils.get_class_name_from_ref_str(self.schema.additionalProperties.ref)
                key_type = PropertyType(self.schema.x_dictionary_key.type).python_type
                placeholders.append(f'{self.name_safe} = dict[{key_type}, {cls_name}]')
            else:
                placeholders.append(f'{self.name_safe} = dict')
        # Enum array placeholder type - These go at the end of the file with the other entity placeholders,
        # for consistency. These do not require it since enums are imported from another file.
        elif self.is_enum_array_placeholder:
            placeholders.append(StringUtils.gen_line_break_comment(self.qualified_name))
            if self.description:
                placeholders.append(StringUtils.gen_comment(self.description))
            enum_name = StringUtils.get_class_name_from_ref_str(self.schema.items.x_enum_reference.ref)
            placeholders.append(f'{self.name_safe} = list[{enum_name}]')
        # Standard entity model
        else:
            body.append(StringUtils.gen_line_break_comment(self.qualified_name))
            if self.allow_extra:
                body += self.default_entity_decorators_with_extra.copy()
            else:
                body += self.default_entity_decorators.copy()

            # Attach the class declaration
            body.append(StringUtils.gen_class_declaration(self.name))

            # Handle the class description as a docstring
            if self.description:
                body.append(StringUtils.gen_docstring(self.description, depth=1))

            if not self.properties:
                body.append(StringUtils.indent_str('pass', 1))
            else:
                body.append('\n'.join(p.field_definition for p in self.properties))
        return '\n'.join(body) if body else None, '\n'.join(placeholders) if placeholders else None

    def _update_placeholder_imports(self, names: list[str]) -> None:
        for prop in self.properties:
            if prop.forward_ref and prop.name in names:
                prop.forward_ref = False

    def _add_property(self, prop: ClassProperty | None) -> None:
        if prop:
            self.properties.append(prop)

    def _add_import(self, imp: EntityImport | None) -> None:
        if imp:
            self.imports.add_import(imp)

    def generate_array_property(self, name: str, prop: Schema) -> None:
        if prop.items.ref:
            self._add_import(EntityImport(name='marshmallow', type=ImportType.external, imports=['fields']))
            self._add_property(ClassProperty(
                name=name,
                type=StringUtils.get_class_name_from_ref_str(prop.items.ref),
                comment=prop.description,
                optional=True,
                list=True,
                forward_ref=True,
            ))
        elif prop.items.x_enum_reference:
            enum_name = StringUtils.get_class_name_from_ref_str(prop.items.x_enum_reference.ref)
            self._add_import(EntityImport(
                name=self.enum_file_name,
                type=ImportType.relative,
                imports=[enum_name]
            ))
            self._add_property(ClassProperty(
                name=name,
                type=enum_name,
                comment=prop.description,
                optional=True,
                list=True,
            ))
        elif PropertyType(prop.items.type) == PropertyType.string:
            self._add_property(ClassProperty(
                name=name,
                type='str',
                comment=prop.description,
                optional=True,
                list=True,
            ))
        elif PropertyType(prop.items.type) == PropertyType.integer:
            self._add_property(ClassProperty(
                name=name,
                type='int',
                comment=prop.description,
                optional=True,
                list=True,
            ))
        elif PropertyType(prop.items.type) == PropertyType.boolean:
            self._add_property(ClassProperty(
                name=name,
                type='bool',
                comment=prop.description,
                optional=True,
                list=True,
            ))
        else:
            print(f'UNHANDLED ARRAY PROPERTY: {self.name} - {name} - {prop}')

    def generate_string_property(self, name: str, prop: Schema) -> None:
        fmt = PropertyFormat(prop.format)
        if fmt == PropertyFormat.datetime:
            self._add_import(EntityImport(name='datetime', type=ImportType.stdlib, imports=['datetime']))
            self._add_import(EntityImport(
                name=f'marshmallow',
                type=ImportType.external,
                imports=['fields']
            ))
            self._add_property(ClassProperty(
                name=name,
                type='datetime',
                comment=prop.description,
                optional=True,
            ))
        elif fmt == PropertyFormat.none:
            self._add_property(ClassProperty(
                name=name,
                type='str',
                comment=prop.description,
                optional=True,
            ))
        elif fmt == PropertyFormat.byte:
            self._add_import(EntityImport(
                name='marshmallow',
                type=ImportType.external,
                imports=['fields']
            ))
            self._add_import(EntityImport(
                name=f'.{self.utils_path_name}.{self.union_field_path_name}',
                type=ImportType.relative,
                imports=['UnionField']
            ))
            self._add_property(ClassProperty(
                name=name,
                type='int | str',
                comment=prop.description,
                optional=True,
                byte=True,
            ))
        else:
            print(f'UNHANDLED STRING FORMAT: {self.name} - {name} - {prop}')

    def generate_number_property(self, name: str, prop: Schema) -> None:
        fmt = PropertyFormat(prop.format)
        if fmt == PropertyFormat.double or fmt == PropertyFormat.float:
            self._add_property(ClassProperty(
                name=name,
                type='float',
                comment=prop.description,
                optional=True,
            ))
        else:
            print(f'UNHANDLED NUMBER FORMAT: {self.name} - {name} - {prop}')

    def generate_integer_property(self, name: str, prop: Schema) -> None:
        if prop.x_enum_reference:
            enum_name = StringUtils.get_class_name_from_ref_str(prop.x_enum_reference.ref)
            self._add_import(EntityImport(
                name=self.enum_file_name,
                type=ImportType.relative,
                imports=[enum_name]
            ))
            fmt = PropertyFormat(prop.format)
            if not fmt == PropertyFormat.byte:
                self._add_property(ClassProperty(
                    name=name,
                    type=enum_name,
                    comment=prop.description,
                    optional=True,
                    enum=True,
                ))
            else:
                self._add_property(ClassProperty(
                    name=name,
                    type=enum_name,
                    comment=prop.description,
                    optional=True,
                    byte_enum=True,
                    enum=True,
                ))
        else:
            self._add_property(ClassProperty(
                name=name,
                type='int',
                comment=prop.description,
                optional=True,
            ))

    def generate_boolean_property(self, name: str, prop: Schema) -> None:
        self._add_property(ClassProperty(
            name=name,
            type='bool',
            comment=prop.description,
            optional=True,
        ))

    def generate_object_property(self, name: str, prop: Schema) -> None:
        if prop.additionalProperties:
            additional_type = PropertyType(prop.additionalProperties.type) if isinstance(prop.additionalProperties, Schema) else None
            if not prop.x_dictionary_key:
                raise TypeError(f'OBJECT SCHEMA PROPERTY HAS NO x-dictionary-key FIELD: {name} {prop}')
            enum_key = False
            byte_enum = False
            if prop.x_dictionary_key.x_enum_reference:
                ref_name = StringUtils.get_class_name_from_ref_str(prop.x_dictionary_key.x_enum_reference.ref)
                self._add_import(EntityImport(name=self.enum_file_name, type=ImportType.relative, imports=[ref_name]))
                key_type = ref_name
                enum_key = True
                if PropertyFormat(prop.x_dictionary_key.format) == PropertyFormat.byte:
                    byte_enum = True
            else:
                key_type = prop.x_dictionary_key.type
            if prop.additionalProperties.ref:
                ref_name = StringUtils.get_class_name_from_ref_str(prop.additionalProperties.ref)
                self._add_import(EntityImport(name='marshmallow', type=ImportType.external, imports=['fields']))
                self._add_property(ClassProperty(
                    name=name,
                    type=ref_name,
                    comment=prop.description,
                    optional=True,
                    dict=True,
                    key_type=key_type,
                    forward_ref=True,
                    enum_key=enum_key,
                    byte_enum=byte_enum,
                ))
            elif additional_type == PropertyType.string:
                self._add_property(ClassProperty(
                    name=name,
                    type='str',
                    comment=prop.description,
                    optional=True,
                    dict=True,
                    key_type=key_type,
                    enum_key=enum_key,
                    byte_enum=byte_enum,
                ))
            elif additional_type == PropertyType.object:
                self._add_import(EntityImport(name='typing', type=ImportType.stdlib, imports=['Any']))
                self._add_property(ClassProperty(
                    name=name,
                    type='Any',
                    comment=prop.description,
                    optional=True,
                    key_type=key_type,
                    enum_key=enum_key,
                    dict=True,
                    byte_enum=byte_enum,
                ))
            elif prop.additionalProperties.x_enum_reference:
                ref_name = StringUtils.get_class_name_from_ref_str(prop.additionalProperties.x_enum_reference.ref)
                self._add_import(EntityImport(name=self.enum_file_name, type=ImportType.relative, imports=[ref_name]))
                self._add_property(ClassProperty(
                    name=name,
                    type=ref_name,
                    comment=prop.description,
                    optional=True,
                    key_type=key_type,
                    enum_key=enum_key,
                    dict=True,
                    byte_enum=byte_enum,
                ))
            elif additional_type == PropertyType.integer:
                self._add_property(ClassProperty(
                    name=name,
                    type='int',
                    comment=prop.description,
                    optional=True,
                    key_type=key_type,
                    enum_key=enum_key,
                    byte_enum=byte_enum,
                    dict=True,
                ))
            elif additional_type == PropertyType.number:
                self._add_property(ClassProperty(
                    name=name,
                    type='float',
                    comment=prop.description,
                    optional=True,
                    dict=True,
                    key_type=key_type,
                    enum_key=enum_key,
                    byte_enum=byte_enum,
                ))
            elif additional_type == PropertyType.boolean:
                self._add_property(ClassProperty(
                    name=name,
                    type='bool',
                    comment=prop.description,
                    optional=True,
                    dict=True,
                    key_type=key_type,
                    enum_key=enum_key,
                    byte_enum=byte_enum,
                ))
            elif additional_type == PropertyType.array:
                if prop.additionalProperties.items and prop.additionalProperties.items.ref:
                    ref_name = StringUtils.get_class_name_from_ref_str(prop.additionalProperties.items.ref)
                    self._add_import(EntityImport(name='marshmallow', type=ImportType.external, imports=['fields']))
                    self._add_property(ClassProperty(
                        name=name,
                        type=ref_name,
                        optional=True,
                        comment=prop.description,
                        dict=True,
                        list=True,
                        key_type=key_type,
                        forward_ref=True,
                        enum_key=enum_key,
                        byte_enum=byte_enum,
                    ))
                else:
                    print(f'UNHANDLED ADDITIONAL PROPERTIES ARRAY OBJECT ENTITY: {self.name} - {name} - {prop}')
            else:
                print(f'UNHANDLED ADDITIONAL PROPERTIES OBJECT ENTITY: {self.name} - {name} - {prop}')
        elif prop.allOf and len(prop.allOf) == 1:
            ref_name = StringUtils.get_class_name_from_ref_str(prop.allOf[0].ref)
            self._add_property(ClassProperty(
                name=name,
                type=ref_name,
                comment=prop.description,
                optional=True,
                forward_ref=True,
            ))
        else:
            print(f'UNHANDLED OBJECT PROPERTY TYPE: {self.name} - {name} - {prop}')

    def generate_ref_property(self, name: str, prop: Schema) -> None:
        ref_name = StringUtils.get_class_name_from_ref_str(prop.ref)
        self._add_import(EntityImport(
            name='dataclasses_json',
            type=ImportType.external,
            imports=['config']
        ))
        self._add_import(EntityImport(
            name='marshmallow',
            type=ImportType.external,
            imports=['fields']
        ))
        self._add_property(ClassProperty(
            name=name,
            type=ref_name,
            comment=prop.description,
            optional=True,
            forward_ref=True,
        ))

    def generate_properties(self) -> None:
        # Object type
        if PropertyType(self.schema.type) == PropertyType.object:
            # Entity object
            if self.schema.properties:
                for k, prop in self.schema.properties.items():
                    prop_type = PropertyType(prop.type)

                    if prop_type == PropertyType.array:
                        self.generate_array_property(k, prop)
                    elif prop_type == PropertyType.string:
                        self.generate_string_property(k, prop)
                    elif prop_type == PropertyType.number:
                        self.generate_number_property(k, prop)
                    elif prop_type == PropertyType.integer:
                        self.generate_integer_property(k, prop)
                    elif prop_type == PropertyType.boolean:
                        self.generate_boolean_property(k, prop)
                    elif prop_type == PropertyType.object:
                        self.generate_object_property(k, prop)
                    elif prop.ref:
                        self.generate_ref_property(k, prop)
                    else:
                        print(f'UNHANDLED PROPERTY TYPE: {self.name} - {k} - {prop}')
            # Placeholder object type
            elif self.is_placeholder:
                pass
            else:
                print(f'OBJECT NOT PROCESSED: {self.name} - {self.schema}')
        # Array type
        elif PropertyType(self.schema.type) == PropertyType.array:
            # Enum reference array placeholder type
            if self.is_enum_array_placeholder:
                ref_name = StringUtils.get_class_name_from_ref_str(self.schema.items.x_enum_reference.ref)
                self._add_import(EntityImport(name=self.enum_file_name, type=ImportType.relative, imports=[ref_name]))
            else:
                print(f'ARRAY NOT PROCESSED: {self.name} - {self.schema}')
        else:
            print(f'UNHANDLED ENTITY TYPE: {self.name} - {self.schema}')


class ResponseEntity(Entity):
    responses_file_name = 'responses'

    def __init__(self, qualified_name: str, response: Response) -> None:
        self.response = response
        super().__init__(qualified_name, response.content['application/json'].schema)

    @property
    def description(self) -> str | None:
        return self.response.description

    @property
    def init_import(self) -> str:
        return EntityImport(
            name=self.responses_file_name,
            type=ImportType.relative,
            imports=[self.name_safe],
        ).import_string

    def generate_array_property(self, name: str, prop: Schema) -> None:
        if prop.items.ref:
            ref_name = StringUtils.get_class_name_from_ref_str(prop.items.ref)
            self._add_import(EntityImport(name=self.entities_file_name, type=ImportType.relative, imports=[ref_name]))
            self._add_property(ClassProperty(
                name=name,
                type=ref_name,
                comment=prop.description,
                optional=True,
                list=True,
            ))
        elif prop.items.x_enum_reference:
            enum_name = StringUtils.get_class_name_from_ref_str(prop.items.x_enum_reference.ref)
            self._add_import(EntityImport(
                name=self.enum_file_name,
                type=ImportType.relative,
                imports=[enum_name]
            ))
            self._add_property(ClassProperty(
                name=name,
                type=enum_name,
                comment=prop.description,
                optional=True,
                list=True,
            ))
        elif PropertyType(prop.items.type) == PropertyType.string:
            self._add_property(ClassProperty(
                name=name,
                type='str',
                comment=prop.description,
                optional=True,
                list=True,
            ))
        elif PropertyType(prop.items.type) == PropertyType.integer:
            self._add_property(ClassProperty(
                name=name,
                type='int',
                comment=prop.description,
                optional=True,
                list=True,
            ))
        elif PropertyType(prop.items.type) == PropertyType.boolean:
            self._add_property(ClassProperty(
                name=name,
                type='bool',
                comment=prop.description,
                optional=True,
                list=True,
            ))
        else:
            print(f'UNHANDLED ARRAY PROPERTY: {self.name} - {name} - {prop}')

    def generate_object_property(self, name: str, prop: Schema) -> None:
        if prop.additionalProperties:
            additional_type = PropertyType(prop.additionalProperties.type) if isinstance(prop.additionalProperties, Schema) else None
            if not prop.x_dictionary_key:
                raise TypeError(f'OBJECT SCHEMA PROPERTY HAS NO x-dictionary-key FIELD: {name} {prop}')
            enum_key = False
            byte_enum = False
            if prop.x_dictionary_key.x_enum_reference:
                ref_name = StringUtils.get_class_name_from_ref_str(prop.x_dictionary_key.x_enum_reference.ref)
                self._add_import(EntityImport(name=self.enum_file_name, type=ImportType.relative, imports=[ref_name]))
                key_type = ref_name
                enum_key = True
                if PropertyFormat(prop.x_dictionary_key.format) == PropertyFormat.byte:
                    self._add_import(EntityImport(name='marshmallow', type=ImportType.external, imports=['fields']))
                    self._add_import(EntityImport(name='dataclasses_json', type=ImportType.external, imports=['config']))
                    byte_enum = True
            else:
                key_type = prop.x_dictionary_key.type
            if prop.additionalProperties.ref:
                ref_name = StringUtils.get_class_name_from_ref_str(prop.additionalProperties.ref)
                self._add_import(EntityImport(name=self.entities_file_name, type=ImportType.relative, imports=[ref_name]))
                self._add_property(ClassProperty(
                    name=name,
                    type=ref_name,
                    comment=prop.description,
                    optional=True,
                    dict=True,
                    key_type=key_type,
                    enum_key=enum_key,
                    byte_enum=byte_enum,
                ))
            elif additional_type == PropertyType.string:
                self._add_property(ClassProperty(
                    name=name,
                    type='str',
                    comment=prop.description,
                    optional=True,
                    dict=True,
                    key_type=key_type,
                    enum_key=enum_key,
                    byte_enum=byte_enum,
                ))
            elif additional_type == PropertyType.object:
                self._add_import(EntityImport(name='typing', type=ImportType.stdlib, imports=['Any']))
                self._add_property(ClassProperty(
                    name=name,
                    type='Any',
                    comment=prop.description,
                    optional=True,
                    key_type=key_type,
                    enum_key=enum_key,
                    byte_enum=byte_enum,
                    dict=True,
                ))
            elif prop.additionalProperties.x_enum_reference:
                ref_name = StringUtils.get_class_name_from_ref_str(prop.additionalProperties.x_enum_reference.ref)
                self._add_import(EntityImport(name=self.enum_file_name, type=ImportType.relative, imports=[ref_name]))
                self._add_property(ClassProperty(
                    name=name,
                    type=ref_name,
                    comment=prop.description,
                    optional=True,
                    key_type=key_type,
                    enum_key=enum_key,
                    byte_enum=byte_enum,
                    dict=True,
                ))
            elif additional_type == PropertyType.integer:
                self._add_property(ClassProperty(
                    name=name,
                    type='int',
                    comment=prop.description,
                    optional=True,
                    key_type=key_type,
                    enum_key=enum_key,
                    byte_enum=byte_enum,
                    dict=True,
                ))
            elif additional_type == PropertyType.number:
                self._add_property(ClassProperty(
                    name=name,
                    type='float',
                    comment=prop.description,
                    optional=True,
                    dict=True,
                    key_type=key_type,
                    enum_key=enum_key,
                    byte_enum=byte_enum,
                ))
            elif additional_type == PropertyType.boolean:
                self._add_property(ClassProperty(
                    name=name,
                    type='bool',
                    comment=prop.description,
                    optional=True,
                    dict=True,
                    key_type=key_type,
                    enum_key=enum_key,
                    byte_enum=byte_enum,
                ))
            elif additional_type == PropertyType.array:
                if prop.additionalProperties.items and prop.additionalProperties.items.ref:
                    ref_name = StringUtils.get_class_name_from_ref_str(prop.additionalProperties.items.ref)
                    self._add_import(EntityImport(name=self.entities_file_name, type=ImportType.relative, imports=[ref_name]))
                    self._add_property(ClassProperty(
                        name=name,
                        type=ref_name,
                        optional=True,
                        comment=prop.description,
                        dict=True,
                        list=True,
                        key_type=key_type,
                        enum_key=enum_key,
                        byte_enum=byte_enum,
                    ))
                else:
                    print(f'UNHANDLED ADDITIONAL PROPERTIES ARRAY OBJECT ENTITY: {self.name} - {name} - {prop}')
            else:
                print(f'UNHANDLED ADDITIONAL PROPERTIES OBJECT ENTITY: {self.name} - {name} - {prop}')
        elif prop.allOf and len(prop.allOf) == 1:
            ref_name = StringUtils.get_class_name_from_ref_str(prop.allOf[0].ref)
            self._add_property(ClassProperty(
                name=name,
                type=ref_name,
                comment=prop.description,
                optional=True,
            ))
        elif not prop.additionalProperties and not prop.allOf and not prop.x_enum_reference:
            self.imports.add_import(EntityImport(name='typing', type=ImportType.stdlib, imports=['Any']))
            self._add_property(ClassProperty(
                name=name,
                type='Any',
                comment=prop.description,
                optional=True,
            ))
        else:
            print(f'UNHANDLED OBJECT PROPERTY TYPE: {self.name} - {name} - {prop}')

    def generate_ref_property(self, name: str, prop: Schema) -> None:
        ref_name = StringUtils.get_class_name_from_ref_str(prop.ref)
        self._add_import(EntityImport(name=self.entities_file_name, type=ImportType.relative, imports=[ref_name]))
        self._add_property(ClassProperty(
            name=name,
            type=ref_name,
            comment=prop.description,
            optional=True,
        ))

    def generate_properties(self) -> None:
        # Object type
        if PropertyType(self.schema.type) == PropertyType.object:
            # Entity object
            if self.schema.properties:
                for k, prop in self.schema.properties.items():
                    prop_type = PropertyType(prop.type)

                    if prop_type == PropertyType.array:
                        self.generate_array_property(k, prop)
                    elif prop_type == PropertyType.string:
                        self.generate_string_property(k, prop)
                    elif prop_type == PropertyType.number:
                        self.generate_number_property(k, prop)
                    elif prop_type == PropertyType.integer:
                        self.generate_integer_property(k, prop)
                    elif prop_type == PropertyType.boolean:
                        self.generate_boolean_property(k, prop)
                    elif prop_type == PropertyType.object:
                        self.generate_object_property(k, prop)
                    elif prop.ref:
                        self.generate_ref_property(k, prop)
                    else:
                        print(f'UNHANDLED PROPERTY TYPE: {self.name} - {k} - {prop}')
            # Placeholder object type
            elif self.is_placeholder:
                pass
            else:
                print(f'OBJECT NOT PROCESSED: {self.name} - {self.schema}')
        # Array type
        elif PropertyType(self.schema.type) == PropertyType.array:
            # Enum reference array placeholder type
            if self.is_enum_array_placeholder:
                ref_name = StringUtils.get_class_name_from_ref_str(self.schema.items.x_enum_reference.ref)
                self._add_import(EntityImport(name=self.enum_file_name, type=ImportType.relative, imports=[ref_name]))
            else:
                print(f'ARRAY NOT PROCESSED: {self.name} - {self.schema}')
        else:
            print(f'UNHANDLED ENTITY TYPE: {self.name} - {self.schema}')


class EntityCollection:
    entities: list[Entity | ResponseEntity]
    imports: EntityImportCollection
    entities_with_extra = ['Queries.PagedQuery']

    def __init__(self):
        self.entities = []
        self.imports = EntityImportCollection()

    @property
    def placeholder_names(self) -> list[str]:
        return [e.name_safe for e in self.entities if e.is_placeholder or e.is_enum_array_placeholder]

    @property
    def entity_models_text_content(self) -> str:
        body = []
        placeholders = []
        for e in self.entities:
            bd, pl = e.formatted_entity
            if bd:
                body.append(bd)
            if pl:
                placeholders.append(pl)

        content = self.imports.formatted_imports
        content += '\n'
        content += '\n\n\n'.join(body)
        if placeholders:
            content += '\n\n\n'
            content += '\n\n'.join(placeholders)
        content += '\n'
        return content

    @property
    def entity_names(self) -> list[str]:
        return [e.name_safe for e in self.entities]

    @property
    def init_imports(self) -> list[str]:
        return [e.init_import for e in self.entities]

    def _update_placeholder_imports(self) -> None:
        for e in self.entities:
            e._update_placeholder_imports(self.placeholder_names)

    def add_entity(self, name: str, schema: Schema) -> None:
        entity = Entity(name, schema, name in self.entities_with_extra)
        self.imports.add_collection(entity.imports)
        self.entities.append(entity)
        self._update_placeholder_imports()

    def add_response(self, name: str, response: Response) -> None:
        res = ResponseEntity(name, response)
        self.imports.add_collection(res.imports)
        self.entities.append(res)

    def write_entity_file(self, file: str) -> None:
        with open(file, 'w+') as entity_file:
            entity_file.write(self.entity_models_text_content)
