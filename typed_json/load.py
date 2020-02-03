from collections import defaultdict
from dataclasses import is_dataclass
from typing import TypeVar, Dict, Union, DefaultDict, List, Tuple, Type, get_type_hints, Optional, Any

T = TypeVar('T')

JsonType = Union[str, int, 'JsonObject']
JsonObject = Dict[str, JsonType]

Errors = DefaultDict[str, Union[List[str], 'Errors']]


class Error:
    MISSING = '__MISSING__'
    INVALID_TYPE = '__INVALID_TYPE__'


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


def _load_field(sources: Dict[str, JsonType], name: str, type_: Type[T]) -> \
        Tuple[Union[Optional[str], 'Errors'], Optional[T]]:
    if name not in sources:
        if _is_optional(type_):
            return None, None
        else:
            return Error.MISSING, None

    source = sources[name]

    if type_ is str:
        return _load_str_field(source)

    return None, sources[name]


def _load_str_field(source: Any) -> Tuple[Optional[str], Optional[T]]:
    if not isinstance(source, str):
        return Error.INVALID_TYPE, source
    return None, source.strip()


def _is_optional(type_: Type[T]) -> bool:
    if getattr(type_, '__origin__', None) != Union:
        return False
    return type(None) in getattr(type_, '__args__', [])
