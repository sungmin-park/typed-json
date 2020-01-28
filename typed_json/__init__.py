from copy import copy
from typing import ClassVar, Dict, Union, TypeVar, Generic, List, Any

ValidJsonType = Union[str]

ErrorType = Union[str]
ErrorsType = List[ErrorType]


class TypedJson:
    _field_prototypes: ClassVar[Dict[str, 'TypedJsonField']]
    _fields: Dict[str, 'TypedJsonField']

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        cls._field_prototypes = dict()
        for name in dir(cls):
            attr = getattr(cls, name)
            if not isinstance(attr, TypedJsonField):
                continue
            delattr(cls, name)
            attr.name = name
            cls._field_prototypes[name] = attr

    def __init__(self):
        self._fields = dict()

        for name, prototype in self._field_prototypes.items():
            field = copy(prototype)
            self._fields[name] = field
            setattr(self, name, field)

    def load(self, source: Dict[str, ValidJsonType]) -> 'TypedJson':
        for name, value in source.items():
            if name not in self._fields:
                continue
            self._fields[name].value = value
        return self

    def dump(self) -> Dict[str, Any]:
        return {field.name: field.value for field in self._fields.values()}

    def validate(self) -> Dict[str, ErrorsType]:
        errors = {}
        for field in self._fields.values():
            field_errors = field.validate()
            if not field_errors:
                continue
            errors[field.name] = field_errors
        return errors


T = TypeVar('T')


class TypedJsonField(Generic[T]):
    name: str
    value: T = None
    optional: bool

    def __init__(self, optional: bool = False):
        self.optional = optional

    def validate(self) -> ErrorsType:
        if self.value is not None or self.optional:
            return []
        return [f'{self.name} field is required']


class String(TypedJsonField[str]):
    pass
