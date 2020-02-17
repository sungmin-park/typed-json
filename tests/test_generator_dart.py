from dataclasses import dataclass

from pytest import raises

from typed_json.generator.dart import convert, DartClass, NotLocalClass, NotNestedClass, DartField
from typed_json.load import NotDataclass, UnknownType


# test convert

@dataclass
class ConverterData:
    string: str


def test_convert():
    assert convert(ConverterData) == DartClass(
        name='ConverterData', location=['tests'], filename='test_generator_dart.dart',
        fields=[DartField(name='string', type_='String')]
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


@dataclass
class UnknownTypeConverterData:
    unknown: object


def test_unknown_type_converter():
    with raises(UnknownType):
        convert(UnknownTypeConverterData)


# test str
@dataclass
class StrData:
    string: str


def test_str():
    assert convert(StrData).fields == [DartField(name='string', type_='String')]


# test to_dart global

def test_to_dart():
    dc = DartClass(name='Person', location=[], filename='',
                   fields=[DartField(name='name', type_='String')])
    assert dc.to_dart_codes() == """\
    class Person {
      String name;
      
      Person(this.name);
    }"""


def test_to_fields():
    dc = DartClass(name='', location=[], filename='', fields=[DartField(name='name', type_='String')])
    assert dc.to_fields() == [
        'String name;',
    ]
