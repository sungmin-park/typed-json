import importlib
from dataclasses import is_dataclass
from typing import Dict, Union, TypeVar, Type, get_type_hints, Any

from stringcase import spinalcase

T = TypeVar('T')
JsonObjectType = Dict[str, 'JsonType']
JsonType = Union[str, Dict[str, Any]]


def load(source: JsonObjectType, target: Type[T]) -> T:
    kwargs = {}
    hints = get_type_hints(target)

    for name, hint in hints.items():
        value = source[spinalcase(name)]
        if is_dataclass(hint):
            cls_name = value['__name__']
            module_name = value['__module__']
            cls = getattr(importlib.import_module(module_name), cls_name)
            value = load(value, cls)
        kwargs[name] = value

    obj = target(**kwargs)
    return obj


def dump(source: T) -> JsonObjectType:
    json = {}
    hints = get_type_hints(source.__class__)

    for name, hint in hints.items():
        value = getattr(source, name)
        if is_dataclass(value):
            class_name = value.__class__.__name__
            module_name = value.__class__.__module__
            value = dump(value)
            value['__name__'] = class_name
            value['__module__'] = module_name
        json[spinalcase(name)] = value

    return json
