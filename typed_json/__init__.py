from collections import defaultdict
from copy import copy
from typing import ClassVar, Dict, Union, TypeVar, Generic, List, Any, DefaultDict, Optional, Iterable, Callable

from stringcase import spinalcase

ValidJsonType = Union[str, int]

ErrorType = Union[str]
ErrorsType = List[ErrorType]


class TypedJson:
    _field_prototypes: ClassVar[Dict[str, 'TypedJsonField']]
    _fields: Dict[str, 'TypedJsonField']

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        cls._field_prototypes = dict()
        for name in dir(cls):
            field = getattr(cls, name)
            if not isinstance(field, TypedJsonField):
                continue
            delattr(cls, name)
            field.name = spinalcase(name)
            cls._field_prototypes[name] = field

    def __init__(self):
        self._fields = dict()

        for name, prototype in self._field_prototypes.items():
            field = copy(prototype)
            if hasattr(field, 'post_copy'):
                field.post_copy()
            self._fields[name] = field
            setattr(self, name, field)

    def load(self, source: Dict[str, ValidJsonType]) -> 'TypedJson':
        for field in self._fields.values():
            if field.name not in source:
                continue
            field.value = source[field.name]
        return self

    def dump(self, typed=False) -> Dict[str, Any]:
        if not typed:
            return {field.name: field.dump() for field in self._fields.values()}
        return {'--name--': self.__class__.__qualname__, '--value--': self.dump()}

    def validate(self) -> 'Errors':
        errors = Errors()
        for field in self._fields.values():
            field_errors = field.validate()
            if not field_errors:
                continue
            errors[field] = field_errors
        self.post_validate(errors)
        return errors

    def post_validate(self, errors: DefaultDict['TypedJsonField', ErrorsType]) -> None:
        """
        Class level validation point. This method will call right after validate.
        :param errors: field errors
        """
        pass


T = TypeVar('T')

Validator = Callable[[Any, ErrorsType], None]


class TypedJsonField(Generic[T]):
    name: str
    value: T = None
    optional: bool
    validators: List[Validator] = list()

    def __init__(self, value: T = None, optional: bool = False, validators: Optional[Iterable[Validator]] = None):
        self.value = value
        self.optional = optional
        if validators is not None:
            self.validators = self.validators + list(validators)

    def validate(self) -> ErrorsType:
        errors = []
        # validate optional
        if self.value is None and not self.optional:
            errors.append(f'{self.name} field is required')

        # default field class validator
        self._validate(errors)

        # custom validator
        for validator in self.validators:
            validator(self, errors)

        return errors

    def _validate(self, errors: ErrorsType) -> None:
        pass

    def dump(self) -> T:
        return self.value


class String(TypedJsonField[str]):
    def _validate(self, errors: ErrorsType) -> None:
        if self.value is not None and not isinstance(self.value, str):
            errors.append(f'{self.name} field should be an string')


class Integer(TypedJsonField[int]):
    def _validate(self, errors: ErrorsType) -> None:
        if self.value is not None and not isinstance(self.value, int):
            errors.append(f'{self.name} field should be an integer number')


U = TypeVar('U', bound=TypedJson)


class Class(TypedJsonField[U]):
    def __init__(self, value: U = None, optional: bool = False,
                 validators: Optional[Iterable[Validator]] = None):
        super().__init__(value, optional, validators)

    def dump(self) -> Dict[str, ValidJsonType]:
        return self.value.dump(typed=True)

    def post_copy(self):
        self.value = copy(self.value)


class Errors(defaultdict, DefaultDict[TypedJsonField, ErrorsType]):
    def __init__(self) -> None:
        super().__init__(list)

    def dump(self) -> Dict[str, ErrorsType]:
        return {field.name: errors for field, errors in self.items()}
