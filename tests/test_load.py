from dataclasses import dataclass
from typing import Optional

from pytest import raises

# noinspection PyProtectedMember
from typed_json.load import load, NotDataclass, _is_optional, Error, _root_type, UnknownType


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


def test_incorrect_type():
    @dataclass
    class Data:
        string: str

    errors, data = load({'string': 1}, Data)
    assert errors == {'string': [Error.INVALID_TYPE]}
    assert data.string == 1


def test_unknown_type_load():
    @dataclass
    class Data:
        unknown: object

    with raises(UnknownType):
        # noinspection PyTypeChecker
        load({'unknown': object()}, Data)


def test_root_type_load():
    """ load 시에 root_type 을 사용해서 Type 을 체크하는지 확인
    Optional[str] 은 str 로 처리되어야 하고, str 의 strip 을 거쳐야 한다.
    """

    @dataclass
    class Data:
        optional_string: Optional[str]

    errors, data = load({'optional_string': ' '}, Data)
    assert errors == {}
    assert data.optional_string == ''


def test_root_type():
    assert _root_type(str) == str
    assert _root_type(Optional[str]) == str


def test_is_optional():
    assert _is_optional(str) is False
    assert _is_optional(Optional[str]) is True


# test str
def test_str_strip():
    @dataclass
    class Data:
        string: str

    errors, data = load({'string': ' str '}, Data)
    assert errors == {}
    assert data.string == 'str'


# test int
def test_int():
    @dataclass
    class Data:
        integer: int

    errors, data = load({'integer': 0}, Data)
    assert errors == {}
    assert data.integer == 0
