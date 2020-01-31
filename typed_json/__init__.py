from typing import Dict, Union, TypeVar, Type, get_type_hints

T = TypeVar('T')
JsonType = Union[str, 'JsonObjectType']
JsonObjectType = Dict[str, JsonType]


def load(source: JsonObjectType, target: Type[T]) -> T:
    obj = target(**source)
    return obj


def dump(source: T) -> JsonObjectType:
    json = {}
    hints = get_type_hints(source.__class__)
    for name, hint in hints.items():
        json[name] = getattr(source, name)
    return json
