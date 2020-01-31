from typing import Dict, Union, TypeVar, Type, get_type_hints

from stringcase import snakecase, spinalcase

T = TypeVar('T')
JsonType = Union[str, 'JsonObjectType']
JsonObjectType = Dict[str, JsonType]


def load(source: JsonObjectType, target: Type[T]) -> T:
    kwargs = {}
    for name, value in source.items():
        kwargs[snakecase(name)] = value
    obj = target(**kwargs)
    return obj


def dump(source: T) -> JsonObjectType:
    json = {}
    hints = get_type_hints(source.__class__)
    for name, hint in hints.items():
        json[spinalcase(name)] = getattr(source, name)
    return json
