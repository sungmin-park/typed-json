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
        first_name = String()
        last_name = String()
        address = String()

    field_name = Person()
    assert field_name.first_name.name == 'first-name'
    assert field_name.last_name.name == 'last-name'
    assert field_name.address.name == 'address'


def test_load():
    class Person(TypedJson):
        first_name = String()
        last_name = String()
        address = String()

    person = Person().load({'first-name': 'John', 'last-name': 'Doe'})
    assert person.first_name.value == 'John'
    assert person.last_name.value == 'Doe'
    assert person.address.value is None


def test_dump():
    class Person(TypedJson):
        first_name = String()
        last_name = String()
        address = String()

    person = Person().load({'first-name': 'John', 'last-name': 'Doe', 'address': 'Seoul, Korea'})

    assert person.dump() == {'first-name': 'John', 'last-name': 'Doe', 'address': 'Seoul, Korea'}


def test_validate():
    class Empty(TypedJson):
        pass

    assert Empty().validate() == dict()

    # optional validation are too many used, so make it as default
    class Person(TypedJson):
        name = String()
        sex = String()
        address = String(optional=True)

    person = Person().load(dict(name='john'))
    assert person.validate() == dict(sex=['sex field is required']), "name was filed and address is optional"
