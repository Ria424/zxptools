__all__ = (
    "MXIProduct",
    "MXIProductName",
)

import re
from typing import Any, Literal, TypeGuard

import attrs

from zxptools.exman.version import ExManVersion

MXIProductName = Literal[
    "Bridge",
    "Contribute",
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


def is_valid_product_name(
    product_name: Any, *, exman_version: ExManVersion | None = None
) -> TypeGuard[MXIProductName]:
    if exman_version is None:
        return (
            product_name == "Bridge"
            or product_name == "Contribute"
            or product_name == "Dreamweaver"
            or product_name == "Fireworks"
            or product_name == "Flash"
            or product_name == "Illustrator"
            or product_name == "Illustrator32"
            or product_name == "Illustrator64"
            or product_name == "InCopy"
            or product_name == "InDesign"
            or product_name == "Photoshop"
            or product_name == "Photoshop32"
            or product_name == "Photoshop64"
            or product_name == "Prelude"
            or product_name == "Premiere"
        )

    if exman_version.value < ExManVersion.CS4.value:
        return (
            product_name == "Dreamweaver"
            or product_name == "Fireworks"
            or product_name == "Flash"
        )
    elif exman_version == ExManVersion.CS4:
        return (
            product_name == "Bridge"
            or product_name == "Contribute"
            or product_name == "Dreamweaver"
            or product_name == "Fireworks"
            or product_name == "Flash"
            or product_name == "Illustrator"
            or product_name == "InCopy"
            or product_name == "InDesign"
            or product_name == "Photoshop32"
            or product_name == "Photoshop64"
        )
    elif exman_version == ExManVersion.CS5:
        return (
            product_name == "Bridge"
            or product_name == "Contribute"
            or product_name == "Dreamweaver"
            or product_name == "Fireworks"
            or product_name == "Flash"
            or product_name == "Illustrator"
            or product_name == "InCopy"
            or product_name == "InDesign"
            or product_name == "Photoshop32"
            or product_name == "Photoshop64"
            or product_name == "Premiere"
        )

    return (
        product_name == "Dreamweaver"
        or product_name == "Fireworks"
        or product_name == "Flash"
        or product_name == "Illustrator"
        or product_name == "Illustrator32"
        or product_name == "Illustrator64"
        or product_name == "InCopy"
        or product_name == "InDesign"
        or product_name == "Photoshop"
        or product_name == "Photoshop32"
        or product_name == "Photoshop64"
        or product_name == "Prelude"
        or product_name == "Premiere"
    )


def attrs_validate_product_name(
    _instance: Any, attribute: attrs.Attribute, value: Any
) -> None:
    if not is_valid_product_name(value):
        raise ValueError(value)


PRODUCT_VERSION_IDENTIFIER_REGEX_PATTERN = re.compile(
    r"^([1-9][0-9]?(?:\.[1-9])?)$"
)


def is_valid_product_version(
    product_version: Any, *, exman_version: ExManVersion
) -> bool:
    return (
        PRODUCT_VERSION_IDENTIFIER_REGEX_PATTERN.match(product_version)
        is not None
    )


@attrs.define
class MXIProduct:
    name: MXIProductName = attrs.field(validator=attrs_validate_product_name)
    """The name of a Macromedia product."""

    version: str
    """
    The major (or sometimes with minor) version number of the specified Macromedia product.
    """

    primary: bool | None = attrs.field(default=None, kw_only=True)
    """
    Whether the specified Macromedia product is the one the extension was \
    primarily intended to be used with.

    ``primary == True`` implies ``required == True`` as well.
    """

    required: bool | None = attrs.field(default=None, kw_only=True)
    """
    Whether the specified Macromedia product is required for the extension to \
    function properly.
    """
