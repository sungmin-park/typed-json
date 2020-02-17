from dataclasses import dataclass

from pytest import raises

from typed_json.dump import dump


def test_dump():
    @dataclass
    class Person:
        name: str

    assert dump(Person(name='john')) == {'name': 'john'}


def test_not_dataclass():
    with raises(ValueError):
        dump(object())
