from typing import Any, get_type_hints

from typed_json.load import JsonObject


def dump(data: Any) -> JsonObject:
    json = {}

    hints = get_type_hints(data)
    for name in hints:
        json[name] = getattr(data, name)

    return json
