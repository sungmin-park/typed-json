from dataclasses import dataclass
from typing import Optional

from pytest import raises

from typed_json import load_, dump_, v, size, NotDataclass


@dataclass
class Person:
    first_name: str
    last_name: str
    age: int
    sex: Optional[str]
    address: 'Address'


@dataclass
class Address:
    street: str


@dataclass
class Request:
    action: 'Action'


@dataclass
class Action:
    pass


@dataclass
class Create(Action):
    name: str


@dataclass
class Update(Create):
    id: int
    name: str


def test_load():
    # test property load
    person, errors = load_(
        {
            'first-name': 'John', 'last-name': 'Doe', 'age': 18,
            'address': {
                '__name__': 'Address', '__module__': 'tests.test_typed_json', 'street': '11 st'
            }
        },
        Person
    )
    assert person == Person(first_name='John', last_name='Doe', age=18, sex=None, address=Address(street='11 st'))
    assert errors == {}

    # test polymorphic load
    request, errors = load_(
        {'action': {'__name__': 'Create', '__module__': 'tests.test_typed_json', 'name': 'initial'}},
        Request
    )
    assert request.action == Create(name='initial')
    assert errors == {}
    request, errors = load_(
        {'action': {'__name__': 'Update', '__module__': 'tests.test_typed_json', 'id': 1, 'name': 'update'}},
        Request
    )
    assert request.action == Update(id=1, name='update')
    assert errors == {}


def test_validate_required():
    person, errors = load_({}, Person)
    assert person.first_name is None
    assert errors == {
        'first-name': ['first-name is required'],
        'last-name': ['last-name is required'],
        'age': ['age is required'],
        'address': ['address is required'],
    }

    # check string length by default
    person, errors = load_({'first-name': ''}, Person)
    assert person.first_name == ''
    assert errors == {
        'first-name': ['first-name is required'],
        'last-name': ['last-name is required'],
        'age': ['age is required'],
        'address': ['address is required'],
    }


def test_class_validation():
    request, errors = load_({'action': 1}, Request)
    assert request.action is None
    assert errors == {'action': ['action should be a dict']}

    request, errors = load_({'action': {'name': 'invalid'}}, Request)
    assert request.action is None
    assert errors == {'action': ['action missing typed-json type information']}

    request, errors = load_({'action': {'__name__': 'backdoor', '__module__': 'danger'}}, Request)
    assert request.action is None
    assert errors == {'action': ['danger module is not imported']}

    request, errors = load_(
        {'action': {'__name__': 'test_class_validation', '__module__': 'tests.test_typed_json'}},
        Request
    )
    assert request.action is None
    assert errors == {'action': ['test_class_validation is not dataclass']}


def test_str():
    @dataclass
    class Data:
        name: Optional[str]

    # str will trim by default
    data, errors = load_({'name': ' _trim_ '}, Data)
    assert errors == {}
    assert data == Data(name='_trim_')


def always_failed(_: str):
    return 'failed'


@dataclass
class Validate:
    name: v(str, always_failed)


def test_validator():
    data, errors = load_({'name': '1234'}, Validate, )
    assert errors == {'name': ['failed']}
    assert data == Validate(name='1234')


def test_dump():
    person = dump_(Person(first_name='John', last_name='Doe', age=18, sex=None, address=Address(street='11 st')))
    assert person == {
        'first-name': 'John', 'last-name': 'Doe', 'age': 18, 'sex': None,
        'address': {
            '__name__': 'Address',
            '__module__': 'tests.test_typed_json',
            'street': '11 st'
        }
    }

    request = dump_(Request(action=Create(name='initial')))
    assert request == {
        'action': {
            '__module__': 'tests.test_typed_json', '__name__': 'Create', 'name': 'initial'
        }
    }
    request = dump_(Request(action=Update(id=1, name='update')))
    assert request == {
        'action': {
            '__module__': 'tests.test_typed_json', '__name__': 'Update', 'id': 1, 'name': 'update'
        }
    }


def test_size():
    @dataclass
    class Size:
        both: v(str, size(5, 10))
        min: v(str, size(min=5))
        max: v(str, size(max=5))
        none: v(str, size())

    _, errors = load_(
        {
            'both': '1234',
            'min': '1234',
            'max': '123456',
            'none': ''
        },
        Size
    )
    assert errors == {
        'both': ['should be greater or equal to 5 and smaller or equal to 10'],
        'min': ['should be greater or equal to 5'],
        'max': ['should be smaller or equal to 5']
    }


def test_data_class_only():
    class BasicClass:
        name: str

    with raises(NotDataclass):
        _ = load_({}, BasicClass)
