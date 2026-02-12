__all__ = (
    "SizedBuffer",
    "StrOrBytesPath",
    "XMLElementLike",
    "XMLDict",
)

from collections.abc import (
    Buffer,
    Iterator,
    Sequence,
    Sized,
)
from os import PathLike
from typing import Protocol, Union

StrOrBytesPath = str | bytes | PathLike[str] | PathLike[bytes]


class SizedBuffer(Sized, Buffer, Protocol):
    pass


class XMLElementLike(Protocol):
    def __iter__(self) -> Iterator["XMLElementLike"]: ...
    def find(self, tag: str) -> "XMLElementLike" | None: ...


XMLDict = Union[
    dict[str, str],
    dict[str, Sequence[str]],
    dict[str, Sequence["XMLDict"]],
    dict[str, "XMLDict"],
]
