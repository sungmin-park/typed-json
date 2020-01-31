from dataclasses import is_dataclass
from typing import Dict, Union, TypeVar, Type, get_type_hints

from stringcase import spinalcase

T = TypeVar('T')
JsonType = Union[str, 'JsonObjectType']
JsonObjectType = Dict[str, JsonType]


def load(source: JsonObjectType, target: Type[T]) -> T:
    kwargs = {}
    hints = get_type_hints(target)
    for name, hint in hints.items():
        value = source[spinalcase(name)]
        if is_dataclass(hint):
            value = load(value, hint)
        kwargs[name] = value
    obj = target(**kwargs)
    return obj


def dump(source: T) -> JsonObjectType:
    json = {}
    hints = get_type_hints(source.__class__)
    for name, hint in hints.items():
        value = getattr(source, name)
        if is_dataclass(value):
            value = dump(value)
        json[spinalcase(name)] = value
    return json
