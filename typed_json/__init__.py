from typing import Dict, Union, TypeVar, Type

T = TypeVar('T')


def load(source: Dict[str, Union[str]], target: Type[T]) -> T:
    obj = target(**source)
    return obj
