__all__ = (
    "SizedBuffer",
    "StrOrBytesPath",
    "XMLElementDataLike",
    "XMLElementData",
    "XMLElementLike",
)

from collections.abc import (
    Buffer,
    Iterator,
    Mapping,
    Sized,
)
from os import PathLike
from typing import Protocol, TypedDict

StrOrBytesPath = str | bytes | PathLike[str] | PathLike[bytes]


class SizedBuffer(Sized, Buffer, Protocol):
    pass


class XMLElementDataLike(Protocol):
    attrib: Mapping[str, str]
    tag: str
    text: str | None


class XMLElementData(TypedDict):
    attrib: Mapping[str, str]
    tag: str
    text: str | None


class XMLElementLike(XMLElementDataLike, Protocol):
    def __iter__(self) -> Iterator["XMLElementLike"]: ...
    def find(self, tag: str) -> "XMLElementLike" | None: ...
