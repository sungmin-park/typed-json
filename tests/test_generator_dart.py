from dataclasses import dataclass

from pytest import raises

from typed_json.generator.dart import convert, DartClass, NotLocalClass, NotNestedClass
from typed_json.load import NotDataclass


@dataclass
class ConverterData:
    string: str


def test_convert():
    assert convert(ConverterData) == DartClass(
        name='ConverterData', location=['tests'], filename='test_generator_dart.dart'
    )


def test_not_dataclass_convert():
    class Data:
        pass

    with raises(NotDataclass):
        convert(Data)


def test_not_local_class_convert():
    @dataclass
    class Data:
        pass

    with raises(NotLocalClass):
        convert(Data)


class NotNestedClassConverter:
    @dataclass
    class Data:
        pass


def test_not_nested_class_convert():
    with raises(NotNestedClass):
        convert(NotNestedClassConverter.Data)
