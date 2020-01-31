from dataclasses import dataclass

from typed_json import load, dump


@dataclass
class Person:
    first_name: str
    last_name: str
    age: int
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
    person = load(
        {
            'first-name': 'John', 'last-name': 'Doe', 'age': 18,
            'address': {
                '__name__': 'Address', '__module__': 'tests.test_typed_json', 'street': '11 st'
            }
        },
        Person
    )
    assert person == Person(first_name='John', last_name='Doe', age=18, address=Address(street='11 st'))

    # test inheritance
    request = load(
        {'action': {'__name__': 'Create', '__module__': 'tests.test_typed_json', 'name': 'initial'}},
        Request
    )
    assert request.action == Create(name='initial')
    request = load(
        {'action': {'__name__': 'Update', '__module__': 'tests.test_typed_json', 'id': 1, 'name': 'update'}},
        Request
    )
    assert request.action == Update(id=1, name='update')


def test_dump():
    person = dump(Person(first_name='John', last_name='Doe', age=18, address=Address(street='11 st')))
    assert person == {
        'first-name': 'John', 'last-name': 'Doe', 'age': 18,
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
