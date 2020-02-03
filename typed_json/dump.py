from dataclasses import is_dataclass
from typing import Any, get_type_hints

from typed_json.load import JsonObject, NotDataclass, _root_type, UnknownType


def dump(data: Any) -> JsonObject:
    if not is_dataclass(data):
        raise NotDataclass(f'dump only works with dataclass, {data.__class__} is not dataclass')
    json = {}

    hints = get_type_hints(data)
    for name, hint in hints.items():
        root_type = _root_type(hint)
        if root_type is not str:
            raise UnknownType(f'Dose not know how to handle {root_type} type')
        json[name] = getattr(data, name)

    return json
