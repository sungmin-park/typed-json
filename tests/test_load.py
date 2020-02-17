from dataclasses import dataclass

from pytest import raises

from typed_json.load import load


def test_load():
    @dataclass
    class Person:
        name: str

    person, errors = load({'name': 'john'}, Person)
    assert errors == {}
    assert person == Person(name='john')


def test_not_dataclass():
    with raises(ValueError):
        load({}, object)
