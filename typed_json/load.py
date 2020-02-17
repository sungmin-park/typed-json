from dataclasses import is_dataclass
from typing import TypeVar, Type, Dict, Any, Tuple, get_type_hints

T = TypeVar('T')


def load(source: Dict[str, Any], cls: Type[T]) -> Tuple[T, Dict[str, Any]]:
    if not is_dataclass(cls):
        raise ValueError(f'class to load is not a dataclass')
    hints = get_type_hints(cls)
    obj = cls(**{name: source[name] for name in hints})
    return obj, {}
