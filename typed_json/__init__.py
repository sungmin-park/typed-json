from copy import copy
from typing import ClassVar, Dict


class TypedJson:
    _fields: ClassVar[Dict[str, 'TypedJsonField']]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        cls._fields = dict()
        for name in dir(cls):
            attr = getattr(cls, name)
            if not isinstance(attr, TypedJsonField):
                continue
            delattr(cls, name)
            attr.name = name
            cls._fields[name] = attr

    def __init__(self):
        for name, field in self._fields.items():
            setattr(self, name, copy(field))


class TypedJsonField:
    name: str


class String(TypedJsonField):
    pass
