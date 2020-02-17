import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Union, Dict

from typing_extensions import Protocol


class Renderer(Protocol):
    @abstractmethod
    def render(self) -> str:
        pass


class Definition(ABC, Renderer):
    pass


@dataclass
class DartClass(Definition):
    name: str

    def render(self) -> str:
        return f'class {self.name} {{}}'


@dataclass
class DartFile(Renderer):
    path: Iterable[str]
    expressions: Iterable[Union[DartClass]] = tuple()

    def render(self) -> str:
        return '\n'.join(expression.render() for expression in self.expressions)


@dataclass
class Dart:
    files: Iterable[DartFile] = tuple()

    def dump(self) -> Dict[Iterable[str], str]:
        return {os.path.join(*file.path) + '.dart': file.render() for file in self.files}
