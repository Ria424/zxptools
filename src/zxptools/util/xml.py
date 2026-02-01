__all__ = (
    "get_attrib",
    "get_bool_attrib",
)

from typing import Literal, overload

from lxml import etree


@overload
def get_attrib(
    element: etree._Element, name: str, *, strict: Literal[False] = ...
) -> str | None: ...


@overload
def get_attrib(
    element: etree._Element, name: str, *, strict: Literal[True] = ...
) -> str: ...


def get_attrib(
    element: etree._Element, name: str, *, strict: bool = False
) -> str | None:
    value = element.get(name)

    if strict and value is None:
        raise KeyError(name)

    if isinstance(value, bytes):
        value = value.decode()

    return value


def get_bool_attrib(element: etree._Element, name: str) -> bool | None:
    attrib = get_attrib(element, name)
    if attrib is None:
        return None
    return attrib == "true"
