from dataclasses import dataclass

from typed_json import load, dump


def test_load():
    @dataclass
    class Address:
        pass

    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int
        address: Address

    person = load({'first-name': 'John', 'last-name': 'Doe', 'age': 18, 'address': {}}, Person)
    assert person == Person(first_name='John', last_name='Doe', age=18, address=Address())


def test_dump():
    @dataclass
    class Address:
        pass

    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int
        address: Address

    person = dump(Person(first_name='John', last_name='Doe', age=18, address=Address()))
    assert person == {'first-name': 'John', 'last-name': 'Doe', 'age': 18, 'address': {}}
