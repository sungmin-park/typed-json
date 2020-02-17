from dataclasses import dataclass

from pytest import raises

from typed_json.dart import dart_class
from typed_json.lang.dart import DartClass


@dataclass
class DartClassPerson:
    pass


def test_dart_class():
    assert dart_class(DartClassPerson) == DartClass(name='DartClassPerson')


def test_not_dataclass():
    with raises(ValueError):
        dart_class(object)
