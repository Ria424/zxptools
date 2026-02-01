import pathlib

__all__ = (
    "MXIFileLike",
    "SizedBuffer",
    "StrOrBytesPath",
    "XMLElementDataLike",
    "XMLElementData",
    "XMLElementLike",
    "XMLMutableMapping",
)

from collections.abc import (
    Buffer,
    Iterator,
    Mapping,
    MutableMapping,
    Sized,
    Sequence,
)
from os import PathLike
from typing import Protocol, TypedDict

StrOrBytesPath = str | bytes | PathLike[str] | PathLike[bytes]


class MXIFileLike(Protocol):
    def get_source(self) -> pathlib.PurePath: ...
    def get_arcname(self) -> pathlib.PurePath: ...
    def get_destination_dirname(self) -> pathlib.PurePath: ...


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


XMLMutableMapping = (
    MutableMapping[str, str]
    | MutableMapping[str, Sequence[str]]
    | MutableMapping[str, "XMLMutableMapping"]
)
