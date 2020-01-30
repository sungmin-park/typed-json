from typing import DefaultDict

from pytest import raises

from typed_json import TypedJson, String, ErrorsType, TypedJsonField, Integer


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
    assert person.validate() == {person.sex: ['sex field is required']}, "name was filed and address is optional"

    # class level validator
    class User(TypedJson):
        id = String()

        password = String()
        password_confirm = String()

        def post_validate(self, errors: DefaultDict[TypedJsonField, ErrorsType]) -> None:
            if self.password in errors or self.password_confirm in errors:
                return

            if self.password.value != self.password_confirm.value:
                errors[self.password_confirm].append('password and password confirm dose not equal')

    user = User().load({'id': 'admin', 'password': '1', 'password-confirm': '2'})
    assert user.validate() == {user.password_confirm: ['password and password confirm dose not equal']}

    # field level validator
    def validate_name(name: String, errors: ErrorsType):
        if name.value == 'admin':
            errors.append('admin is not allowed')

    class Person(TypedJson):
        name = String(validators=[validate_name])

    person = Person().load(dict(name='admin'))
    assert person.validate() == {person.name: ['admin is not allowed']}


def test_errors_dump():
    class Person(TypedJson):
        name = String()

    assert Person().load(dict()).validate().dump() == {'name': ['name field is required']}


def test_int():
    class Person(TypedJson):
        age = Integer()

    assert Person().load(dict(age=1)).age.value == 1

    person = Person().load(dict(age='1'))
    assert person.validate() == {person.age: ['age field should be an integer number']}
    assert person.age.value == '1'

    # int validate should not works None
    person = Person()
    assert person.validate() == {person.age: ['age field is required']}


def test_str():
    class Person(TypedJson):
        name = String()

    assert Person().load({'name': 'John'}).name.value == 'John'

    person = Person().load(dict(name=True))
    assert person.validate() == {person.name: ['name field should be an string']}

    # String validate should not works None
    person = Person()
    assert person.validate() == {person.name: ['name field is required']}
