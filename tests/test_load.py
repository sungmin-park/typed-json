from dataclasses import dataclass

from pytest import raises

from typed_json.load import load, NotDataclass


def test_emtpy_load():
    # test emtpy class for signature
    @dataclass
    class Empty:
        pass

    errors, empty = load({}, Empty)
    assert errors == {}
    assert isinstance(empty, Empty)


def test_basic_load():
    # test single property for basic load
    @dataclass
    class Person:
        name: str

    errors, person = load({'name': 'john'}, Person)
    assert errors == {}
    assert person.name == 'john'


def test_not_dataclass_load():
    class Emtpy:
        pass

    with raises(NotDataclass):
        load({}, Emtpy)


def test_missing_load():
    @dataclass
    class Person:
        name: str

    errors, person = load({}, Person)
    assert errors == {'name': ['__missing__']}
    assert person.name is None
