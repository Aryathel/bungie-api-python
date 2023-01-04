from enum import Enum


class ImportType(Enum):
    stdlib = 1
    external = 2
    internal = 3
    relative = 4


class PropertyType(Enum):
    none = None
    array = "array"
    string = "string"
    number = "number"
    integer = "integer"
    boolean = "boolean"
