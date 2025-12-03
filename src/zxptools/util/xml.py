__all__ = (
    "get_attrib",
    "get_bool_attrib",
)

from lxml import etree


def get_attrib(element: etree._Element, name: str) -> str:
    value = element.get(name)

    if value is None:
        raise KeyError(name)

    if isinstance(value, bytes):
        value = value.decode()

    return value


def get_bool_attrib(element: etree._Element, name: str) -> bool:
    return get_attrib(element, name) == "true"
