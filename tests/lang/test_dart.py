from typed_json.lang.dart import DartClass, DartFile, Dart


def test_dart_class_empty():
    assert DartClass(name='TestDartClassEmpty').render() == 'class TestDartClassEmpty {}'


# Dart Package

def test_dart_file_empty():
    assert DartFile(path=['dart_file_emtpy']).render() == ''


def test_dart_file():
    assert DartFile(path=['dart_file'], expressions=[DartClass('DartClass')]).render() == 'class DartClass {}'


# Dart

def test_dart_empty():
    assert Dart().dump() == {}


def test_dart():
    assert Dart(files=[DartFile(path=['dart_file'])]).dump() == {'dart_file.dart': ''}
