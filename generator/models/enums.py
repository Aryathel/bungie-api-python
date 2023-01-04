from datetime import datetime
from enum import Enum
from typing import Type, Any


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
    object = "object"


class PropertyFormat(Enum):
    none = None
    int16 = "int16"
    int32 = "int32"
    int64 = "int64"
    uint32 = "uint32"
    float = "float"
    double = "double"
    byte = "byte"
    date = "date"
    datetime = "date-time"

    @property
    def type(self) -> Type[Any]:
        if self in [PropertyFormat.int16, PropertyFormat.int32, PropertyFormat.int64, PropertyFormat.uint32]:
            return int
        elif self in [PropertyFormat.float, PropertyFormat.double]:
            return float
        elif self in [PropertyFormat.byte]:
            return str
        elif self in [PropertyFormat.date, PropertyFormat.datetime]:
            return datetime
        else:
            return None
