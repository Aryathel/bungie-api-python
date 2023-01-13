from typing import Type

from marshmallow.exceptions import ValidationError


def dict_union_dataclass_decoder(key_type: Type, *types: Type):
    def decode(val: dict):
        if not val:
            return val
        obj = {}
        for k, v in val.items():
            k = key_type(k)
            last_err = None
            for type in types:
                try:
                    obj[k] = type.schema().load(v)
                except ValidationError as e:
                    last_err = e
            if k not in obj:
                print(f'Failed to decode value {k}: {v}')
                raise last_err
        return obj
    return decode


def list_union_dataclass_decoder(*types: Type):
    def decode(val: list):
        if not val:
            return val
        vals = []
        for v in val:
            processed = False
            for type in types:
                try:
                    vals.append(type.from_dict(v))
                    processed = True
                except KeyError:
                    pass
            if not processed:
                raise ValueError(f'Failed to decode value {v}')
        return vals
    return decode


def union_dataclass_decoder(*types: Type):
    def decode(val: dict):
        if not val:
            return val
        for type in types:
            try:
                return type.from_dict(val)
            except KeyError:
                pass
        raise ValueError(f'Failed to decode value {val}')
    return decode
