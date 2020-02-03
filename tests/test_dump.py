from dataclasses import dataclass

from pytest import raises

from typed_json.dump import dump
from typed_json.load import NotDataclass, UnknownType


# test dump
def test_basic_dump():
    @dataclass
    class Person:
        name: str

    assert dump(Person(name='john')) == {'name': 'john'}


def test_not_dataclass():
    class Data:
        pass

    with raises(NotDataclass):
        dump(Data())


def test_unknown_type():
    @dataclass
    class Data:
        value: object

    with raises(UnknownType):
        dump(Data(value=object()))
