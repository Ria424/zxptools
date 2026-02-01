__all__ = (
    "MXIProduct",
    "MXIProductName",
)

from typing import Literal

import attrs

MXIProductName = Literal[
    "Dreamweaver",
    "Fireworks",
    "Flash",
    "Illustrator",  # (Illustrator in Mac OS)
    "Illustrator32",  # (32-bit Illustrator in Windows)
    "Illustrator64",  # (64-bit Illustrator in Windows)
    "InCopy",
    "InDesign",
    "Photoshop",  # (Photoshop in Mac OS)
    "Photoshop32",  # (32-bit Photoshop in Windows)
    "Photoshop64",  # (64-bit Photoshop in Windows)
    "Prelude",
    "Premiere",
]


@attrs.define
class MXIProduct:
    name: MXIProductName
    version: str
    primary: bool | None = None
    required: bool | None = None
