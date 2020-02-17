from dataclasses import dataclass

from pytest import raises

from typed_json.dart import dart_class
from typed_json.lang.dart import DartClass


@dataclass
class TestDartPerson:
    pass


def test_dart():
    assert dart_class(TestDartPerson) == DartClass(name='TestDartPerson')


def test_not_dataclass():
    with raises(ValueError):
        dart_class(object)
