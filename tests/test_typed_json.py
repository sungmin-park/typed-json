from dataclasses import dataclass

from typed_json import load


def test_integration():
    @dataclass
    class Person:
        name: str
        age: int

    person = load(dict(name='john', age=18), Person)
    assert person.name == 'john'
    assert person.age == 18


def test_load():
    @dataclass
    class Person:
        name: str
        age: int

    person = load(dict(name='john', age=18), Person)
    assert person.name == 'john'
    assert person.age == 18
