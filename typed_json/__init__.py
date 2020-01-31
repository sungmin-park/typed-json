import sys
from collections import defaultdict
from dataclasses import is_dataclass
from typing import Dict, Union, TypeVar, Type, get_type_hints, Tuple, List, DefaultDict

from stringcase import spinalcase

T = TypeVar('T')
JsonObjectType = Dict[str, 'JsonType']
JsonType = Union[str, int, Dict[str, JsonObjectType]]

Errors = DefaultDict[str, Union[List[str], 'Errors']]


def load(source: JsonObjectType, target: Type[T]) -> Tuple[T, Errors]:
    kwargs = {}
    hints = get_type_hints(target)

    errors = defaultdict(list)
    for name, hint in hints.items():
        json_name = spinalcase(name)
        if json_name not in source:
            kwargs[name] = None
            if type(None) not in getattr(hint, '__args__', []):
                errors[json_name].append(f'{json_name} is required')
            continue

        value = source[json_name]

        if is_dataclass(hint):
            if not isinstance(value, dict):
                kwargs[name] = None
                errors[name].append(f'{json_name} should be a dict')
                continue
            cls_name = value.get('__name__', None)
            module_name = value.get('__module__', None)
            if not isinstance(cls_name, str) or not isinstance(module_name, str):
                kwargs[name] = None
                errors[name].append(f'{json_name} missing typed-json type information')
                continue
            # 미리 임포트 되어 있는 module 만 사용할 수 있도록 강제한다.
            if module_name not in sys.modules:
                kwargs[name] = None
                errors[name].append(f'{module_name} module is not imported')
                continue
            cls = getattr(sys.modules[module_name], cls_name, None)
            if not is_dataclass(cls):
                kwargs[name] = None
                errors[name].append(f'{cls_name} is not dataclass')
                continue
            value, value_errors = load(value, cls)
        elif hint == str or str in getattr(hint, '__args__', []):
            if value is not None:
                value = value.strip()
        kwargs[name] = value

    obj = target(**kwargs)
    return obj, errors


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
