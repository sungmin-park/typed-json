from dataclasses import dataclass

from typed_json.dump import dump


def test_basic_dump():
    @dataclass
    class Person:
        name: str

    assert dump(Person(name='john')) == {'name': 'john'}
