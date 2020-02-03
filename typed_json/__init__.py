import sys
from collections import defaultdict
from dataclasses import is_dataclass, dataclass, field
from typing import Dict, Union, TypeVar, Type, get_type_hints, Tuple, List, DefaultDict, Callable, Optional, NewType, \
    Any

from stringcase import spinalcase

T = TypeVar('T')
JsonObjectType = Dict[str, 'JsonType']
JsonType = Union[str, int, Dict[str, JsonObjectType]]

Errors = DefaultDict[str, Union[List[str], 'Errors']]
Validator = Callable[[T], Union[str, List[str]]]


class NotDataclass(ValueError):

    def __init__(self, *args) -> None:
        super().__init__(*args)


def load_(source: JsonObjectType, target: Type[T]) -> Tuple[T, Errors]:
    kwargs = {}
    hints = get_type_hints(target)

    errors = defaultdict(list)

    if not is_dataclass(target):
        raise NotDataclass(f'target should be a dataclass {target}')

    for name, hint in hints.items():
        json_name = spinalcase(name)
        if json_name not in source:
            value = None
            if type(None) not in getattr(hint, '__args__', []):
                errors[json_name].append(f'{json_name} is required')
        else:
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
                value, value_errors = load_(value, cls)
            elif hint == str or str in getattr(hint, '__args__', []):
                if value is not None:
                    value = value.strip()
                if not value:
                    errors[json_name].append(f'{json_name} is required')
        kwargs[name] = value

        typed_json: TypedJson = getattr(hint, '__typed_json__', None)
        if typed_json:
            for validator in typed_json.validators:
                error = validator(value)
                if error:
                    errors[json_name].append(error)

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


@dataclass
class TypedJson:
    validators: List[Callable[[Any], str]] = field(default_factory=list)


def v(type_: Type[T], *validators: Callable[[Optional[T]], Optional[str]]) -> Type[T]:
    if hasattr(type_, '__supertype__'):
        new_type = type_
    else:
        new_type = NewType(f'validated-{str(type_)}', type_)
    if not hasattr(new_type, '__typed_json__'):
        new_type.__typed_json__ = TypedJson()
    new_type.__typed_json__.validators.extend(validators)
    return new_type


# noinspection PyShadowingBuiltins
def size(min: Optional[int] = None, max: Optional[int] = None) -> Callable[[Optional[str]], Optional[str]]:
    if min is None and max is None:
        return lambda _: None

    if max is None:
        def validate(value: Optional[str]):
            if not value or len(value) >= min:
                return None
            return f'should be greater or equal to {min}'
    elif min is None:
        def validate(value: Optional[str]):
            if not value or len(value) <= max:
                return None
            return f'should be smaller or equal to {max}'
    else:
        def validate(value: Optional[str]):
            if not value or min <= len(value) <= max:
                return None
            return f'should be greater or equal to {min} and smaller or equal to {max}'

    return validate
