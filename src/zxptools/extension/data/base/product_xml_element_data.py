__all__ = ("ProductElement",)

from typing import Literal, TypedDict

from zxptools.type import XMLElementData


class ProductElement:
    __slots__ = (
        "name",
        "primary",
        "version",
    )

    def __init__(self, *, name: str, version: str, primary: bool) -> None:
        self.name = name
        self.version = version
        self.primary = primary

    def dump(self) -> XMLElementData:
        return {
            "attrib": {
                "name": self.name,
                "version": self.version,
                "primary": "true" if self.primary else "false",
            },
            "tag": "product",
            "text": None,
        }


class ProductXMLElementDataAttrib(TypedDict):
    name: str
    version: str
    primary: Literal["true", "false"]


class ProductXMLElementData(XMLElementData):
    attrib: ProductXMLElementDataAttrib
    tag: Literal["product"]
    text: None
