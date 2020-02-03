from dataclasses import dataclass
from typing import Optional

from pytest import raises

# noinspection PyProtectedMember
from typed_json.load import load, NotDataclass, _is_optional, Error


# Test Default load behaviors
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
    assert errors == {'name': [Error.MISSING]}
    assert person.name is None


def test_missing_optional_load():
    @dataclass
    class Person:
        name: Optional[str]

    errors, person = load({}, Person)
    assert errors == {}
    assert person.name is None


def test_is_optional():
    assert _is_optional(str) is False
    assert _is_optional(Optional[str]) is True


# Test str
def test_str_incorrect_type():
    @dataclass
    class Data:
        not_str: str

    errors, data = load({'not_str': 1}, Data)
    assert errors == {'not_str': [Error.INVALID_TYPE]}
    assert data.not_str == 1
