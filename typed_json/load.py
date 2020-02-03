from collections import defaultdict
from dataclasses import is_dataclass
from typing import TypeVar, Dict, Union, DefaultDict, List, Tuple, Type, get_type_hints, Optional

T = TypeVar('T')

JsonType = Union[str, 'JsonObject']
JsonObject = Dict[str, JsonType]

Errors = DefaultDict[str, Union[List[str], 'Errors']]


class Error:
    MISSING = '__MISSING__'


class NotDataclass(ValueError):
    pass


def load(source: Dict[str, JsonType], type_: Type[T]) -> Tuple[Errors, T]:
    if not is_dataclass(type_):
        raise NotDataclass(f'load type_ only works with dataclass')

    properties = {}
    errors = defaultdict(list)
    for name, hint in get_type_hints(type_).items():
        filed_error, field_value = _load_field(source, name, hint)
        if filed_error:
            errors[name].append(filed_error)
        properties[name] = field_value

    return errors, type_(**properties)


def _load_field(source: Dict[str, JsonType], name: str, type_: Type[T]) -> \
        Tuple[Union[Optional[str], 'Errors'], Optional[T]]:
    if name not in source:
        if _is_optional(type_):
            return None, None
        else:
            return Error.MISSING, None

    return None, source[name]


def _is_optional(type_: Type[T]) -> bool:
    if getattr(type_, '__origin__', None) != Union:
        return False
    return type(None) in getattr(type_, '__args__', [])
