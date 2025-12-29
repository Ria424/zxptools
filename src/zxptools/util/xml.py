__all__ = (
    "get_attrib",
    "get_bool_attrib",
)

from typing import Any

from lxml import etree

from zxptools.type import XMLElementData


def get_attrib(element: etree._Element, name: str) -> str:
    value = element.get(name)

    if value is None:
        raise KeyError(name)

    if isinstance(value, bytes):
        value = value.decode()

    return value


def get_bool_attrib(element: etree._Element, name: str) -> bool:
    return get_attrib(element, name) == "true"


def sub_element_from_dict(parent: Any, dict_: XMLElementData):
    return etree.SubElement(parent, _tag=dict_["tag"], attrib=dict_["attrib"])
