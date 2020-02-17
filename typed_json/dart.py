from dataclasses import is_dataclass
from typing import Type, Any

from typed_json.lang.dart import DartClass


def dart_class(cls: Type[Any]) -> DartClass:
    if not is_dataclass(cls):
        raise ValueError('class is not a dataclass')

    return DartClass(name=cls.__name__)
