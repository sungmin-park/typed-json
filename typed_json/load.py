from collections import defaultdict
from dataclasses import is_dataclass
from typing import TypeVar, Dict, Union, DefaultDict, List, Tuple, Type, get_type_hints, Optional

T = TypeVar('T')

JsonType = Union[str, int, 'JsonObject']
JsonObject = Dict[str, JsonType]

Errors = DefaultDict[str, Union[List[str], 'Errors']]


class Error:
    MISSING = '__MISSING__'
    INVALID_TYPE = '__INVALID_TYPE__'


class NotDataclass(ValueError):
    pass


class UnknownType(ValueError):
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


def _load_field(sources: Dict[str, JsonType], name: str, type_: Type[T]) -> \
        Tuple[Union[Optional[str], 'Errors'], Optional[T]]:
    if name not in sources:
        if _is_optional(type_):
            return None, None
        else:
            return Error.MISSING, None

    source = sources[name]

    root_type = _root_type(type_)
    if type(source) != root_type:
        return Error.INVALID_TYPE, source

    if root_type is str:
        return None, source.strip()

    if root_type is int:
        return None, source

    raise UnknownType(f'Dose not know how to handle {root_type} type')


def _is_optional(type_: Type[T]) -> bool:
    if getattr(type_, '__origin__', None) != Union:
        return False
    return type(None) in getattr(type_, '__args__', [])


def _root_type(type_: Type[T]) -> T:
    if hasattr(type_, '__args__'):
        return _root_type(type_.__args__[0])
    return type_
