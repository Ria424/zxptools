__all__ = (
    "SizedBuffer",
    "StrOrBytesPath",
)

from collections.abc import Buffer, Sized
from os import PathLike
from typing import Protocol

StrOrBytesPath = str | bytes | PathLike[str] | PathLike[bytes]


class SizedBuffer(Sized, Buffer, Protocol):
    pass
