from pytest import raises

from typed_json import TypedJson, String


def test_class_field_access():
    class Person(TypedJson):
        name = String()

    # Prevent direct field access, initialized Field instance will cloned on every instance
    with raises(AttributeError):
        assert isinstance(Person.name, String)

    john = Person()
    assert isinstance(john.name, String), "Instance field should be accessible."
    jane = Person()
    assert jane.name is not john.name, "field will copied from original, so must be different."
    assert jane.name.name is john.name.name, "shallow copy will makes attribute values all same"

    john.name.value = 'john'
    jane.name.value = 'jane'
    assert john.name.value != jane.name.value, "In different instance values should be different."


def test_field_name():
    class Person(TypedJson):
        name = String()
        address = String()

    field_name = Person()
    assert field_name.name.name == 'name'
    assert field_name.address.name == 'address'


def test_load():
    class Person(TypedJson):
        name = String()
        address = String()

    person = Person().load(dict(name='이름'))
    assert person.name.value == '이름'
    assert person.address.value is None


def test_validate():
    class Empty(TypedJson):
        pass

    assert Empty().validate() == dict()

    class Person(TypedJson):
        name = String()
        sex = String()
        address = String(optional=True)

    person = Person().load(dict(name='john'))
    assert person.validate() == dict(sex=['sex field is required']), "name is filed and address is optional"
