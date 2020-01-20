from pytest import raises

from typed_json import TypedJson, String


class Person(TypedJson):
    name = String()
    address = String()


def test_class_field_access():
    # Prevent direct field access, initialized Field instance will cloned on every instance
    with raises(AttributeError):
        assert isinstance(Person.name, String)

    john = Person()
    assert isinstance(john.name, String), "Instance field should be accessible."
    jane = Person()
    assert jane.name is not john.name, "field will copied from original, so must be different."
    assert jane.name.name is john.name.name, "shallow copy will makes attribute values all same"


def test_field_name():
    assert Person().name.name == 'name'
    assert Person().address.name == 'address'
