from dataclasses import is_dataclass, dataclass
from typing import Type, Any, List, get_type_hints

from typed_json.load import NotDataclass, _root_type, UnknownType


class NotLocalClass(ValueError):
    pass


class NotNestedClass(ValueError):
    pass


@dataclass
class DartClass:
    name: str
    location: List[str]
    filename: str
    fields: List['DartField']


@dataclass
class DartField:
    name: str
    type_: str


def convert(type_: Type[Any]) -> DartClass:
    if not is_dataclass(type_):
        raise NotDataclass(f'convert only works with dataclass, {type_} is not dataclass')

    class_name = type_.__qualname__
    if '<locals>' in class_name:
        raise NotLocalClass(f'convert only works with not local dataclasses')
    if '.' in class_name:
        raise NotNestedClass(f'convert only works with not nested dataclasses')

    path = type_.__module__.split('.')
    location = path[:-1]
    filename = f'{path[-1]}.dart'

    fields = []
    for name, hint in get_type_hints(type_).items():
        root_type = _root_type(hint)
        if root_type == str:
            field_type = 'String'
        else:
            raise UnknownType(f'Dose not know how to handle {root_type} type')
        fields.append(DartField(name=name, type_=field_type))

    return DartClass(name=class_name, location=location, filename=filename, fields=fields)
