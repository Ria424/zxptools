__all__ = (
    "get_attrib",
    "get_bool_attrib",
)

from typing import Literal, overload

from lxml import etree


@overload
def get_attrib(
    element: etree._Element,
    name: str,
    *,
    default: str,
    strict: Literal[False] = ...,
) -> str: ...


@overload
def get_attrib(
    element: etree._Element,
    name: str,
    *,
    default: None,
    strict: Literal[False] = ...,
) -> str | None: ...


@overload
def get_attrib(
    element: etree._Element,
    name: str,
    *,
    default: None = None,
    strict: Literal[True] = ...,
) -> str: ...


def get_attrib(
    element: etree._Element,
    name: str,
    *,
    default: str | None = None,
    strict: bool = False,
) -> str | None:
    value = element.get(name)

    if value is None:
        if strict:
            raise KeyError(name)
        return default

    if isinstance(value, bytes):
        value = value.decode()

    return value


@overload
def get_bool_attrib(
    element: etree._Element, name: str, *, default: bool
) -> bool: ...


@overload
def get_bool_attrib(
    element: etree._Element, name: str, *, default: None = None
) -> bool | None: ...


def get_bool_attrib(
    element: etree._Element, name: str, *, default: bool | None = None
) -> bool | None:
    attrib = get_attrib(element, name)
    if attrib is None:
        return default
    return attrib == "true"
