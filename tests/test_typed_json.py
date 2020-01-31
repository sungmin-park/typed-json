from dataclasses import dataclass

from typed_json import load, dump


def test_load():
    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int

    person = load({'first-name': 'John', 'last-name': 'Doe', 'age': 18}, Person)
    assert person == Person(first_name='John', last_name='Doe', age=18)


def test_dump():
    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int

    person = dump(Person(first_name='John', last_name='Doe', age=18))
    assert person == {'first-name': 'John', 'last-name': 'Doe', 'age': 18}
