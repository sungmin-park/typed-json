from dataclasses import is_dataclass, dataclass
from typing import Type, Any, List

from typed_json.load import NotDataclass


class NotLocalClass(ValueError):
    pass


class NotNestedClass(ValueError):
    pass


@dataclass
class DartClass:
    name: str
    location: List[str]
    filename: str


def convert(type_: Type[Any]) -> DartClass:
    if not is_dataclass(type_):
        raise NotDataclass(f'convert only works with dataclass, {type_} is not dataclass')

    name = type_.__qualname__
    if '<locals>' in name:
        raise NotLocalClass(f'convert only works with not local dataclasses')
    if '.' in name:
        raise NotNestedClass(f'convert only works with not nested dataclasses')

    path = type_.__module__.split('.')
    location = path[:-1]
    filename = f'{path[-1]}.dart'
    return DartClass(name=name, location=location, filename=filename)
