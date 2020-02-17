from dataclasses import is_dataclass
from typing import Dict, Any, get_type_hints


def dump(obj: Any) -> Dict[str, Any]:
    if not is_dataclass(obj):
        raise ValueError('dump object is not a dataclass')

    hints = get_type_hints(obj)
    return {name: getattr(obj, name) for name in hints}
