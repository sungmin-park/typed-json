from dataclasses import dataclass
from typing import Optional

from typed_json import load, dump


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
    person, errors = load(
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

    # test inheritance
    request, errors = load(
        {'action': {'__name__': 'Create', '__module__': 'tests.test_typed_json', 'name': 'initial'}},
        Request
    )
    assert request.action == Create(name='initial')
    assert errors == {}
    request, errors = load(
        {'action': {'__name__': 'Update', '__module__': 'tests.test_typed_json', 'id': 1, 'name': 'update'}},
        Request
    )
    assert request.action == Update(id=1, name='update')
    assert errors == {}


def test_validate_required():
    person, errors = load({}, Person)
    assert person.first_name is None
    assert errors == {
        'first-name': ['first-name is required'],
        'last-name': ['last-name is required'],
        'age': ['age is required'],
        'address': ['address is required'],
    }


def test_class_validation():
    request, errors = load({'action': 1}, Request)
    assert request.action is None
    assert errors == {'action': ['action should be a dict']}

    request, errors = load({'action': {'name': 'invalid'}}, Request)
    assert request.action is None
    assert errors == {'action': ['action missing typed-json type information']}

    request, errors = load({'action': {'__name__': 'backdoor', '__module__': 'danger'}}, Request)
    assert request.action is None
    assert errors == {'action': ['danger module is not imported']}

    request, errors = load(
        {'action': {'__name__': 'test_class_validation', '__module__': 'tests.test_typed_json'}},
        Request
    )
    assert request.action is None
    assert errors == {'action': ['test_class_validation is not dataclass']}


def test_trim_str():
    @dataclass
    class Data:
        name: Optional[str]

    data, errors = load({'name': ' _trim_ '}, Data)
    assert errors == {}
    assert data == Data(name='_trim_')


def test_dump():
    person = dump(Person(first_name='John', last_name='Doe', age=18, sex=None, address=Address(street='11 st')))
    assert person == {
        'first-name': 'John', 'last-name': 'Doe', 'age': 18, 'sex': None,
        'address': {
            '__name__': 'Address',
            '__module__': 'tests.test_typed_json',
            'street': '11 st'
        }
    }

    request = dump(Request(action=Create(name='initial')))
    assert request == {
        'action': {
            '__module__': 'tests.test_typed_json', '__name__': 'Create', 'name': 'initial'
        }
    }
    request = dump(Request(action=Update(id=1, name='update')))
    assert request == {
        'action': {
            '__module__': 'tests.test_typed_json', '__name__': 'Update', 'id': 1, 'name': 'update'
        }
    }
