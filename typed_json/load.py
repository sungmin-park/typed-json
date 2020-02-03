from collections import defaultdict
from dataclasses import is_dataclass
from typing import TypeVar, Dict, Union, DefaultDict, List, Tuple, Type, get_type_hints

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
    for name in get_type_hints(type_):
        properties[name] = source[name]

    return defaultdict(list), type_(**properties)
