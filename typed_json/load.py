from collections import defaultdict
from dataclasses import is_dataclass
from typing import TypeVar, Dict, Union, DefaultDict, List, Tuple, Type, get_type_hints, Optional

T = TypeVar('T')

JsonType = Union[str, 'JsonObject']
JsonObject = Dict[str, JsonType]

Errors = DefaultDict[str, Union[List[str], 'Errors']]


class NotDataclass(ValueError):
    pass


def load(source: Dict[str, JsonType], type_: Type[T]) -> Tuple[Errors, T]:
    if not is_dataclass(type_):
        raise NotDataclass(f'load type_ only works with dataclass')

    properties = {}
    errors = defaultdict(list)
    for name in get_type_hints(type_):
        filed_error, field_value = _load_field(source, name)
        if filed_error:
            errors[name].append(filed_error)
        properties[name] = field_value

    return errors, type_(**properties)


def _load_field(source: Dict[str, JsonType], name: str) -> Tuple[Union[Optional[str], 'Errors'], T]:
    if name not in source:
        return '__missing__', None

    return None, source[name]
