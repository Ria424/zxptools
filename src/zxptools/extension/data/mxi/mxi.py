__all__ = ("MXI",)

from collections.abc import MutableSequence
from typing import IO, Literal

from lxml import etree

from zxptools import util
from zxptools.extension.data.base import (
    BaseExtensionInfo,
    ProductElement,
)
from zxptools.extension.data.mxi.file_element import MXIFileElement
from zxptools.type import StrOrBytesPath


class MXI(BaseExtensionInfo):
    __slots__ = ("files",)

    def __init__(
        self,
        /,
        name: str,
        version: str,
        type_: Literal["command", "flashpanel"],
        requires_restart: bool,
        locked: bool,
        *,
        author: str | None = None,
        description: str | None = None,
        files: MutableSequence[MXIFileElement] | None = None,
        license_agreement: str | None = None,
        products: MutableSequence[ProductElement] | None = None,
        signatures: str | None = None,
        ui_access: str | None = None,
        update: str | None = None,
    ) -> None:
        self.name = name
        self.version = version
        self.type = type_
        self.requires_restart = requires_restart
        self.locked = locked
        self.author = author
        self.description = description
        self.files: MutableSequence[MXIFileElement] = (
            files if files is not None else []
        )
        self.license_agreement = license_agreement
        self.products: MutableSequence[ProductElement] = (
            products if products is not None else []
        )
        self.signatures = signatures
        self.ui_access = ui_access
        self.update = update

    @classmethod
    def load(cls, source: StrOrBytesPath | IO[str] | IO[bytes]) -> "MXI":
        element_tree = etree.parse(
            source,
            parser=etree.XMLParser(
                encoding="UTF-8",
                remove_blank_text=True,
                remove_comments=True,
                strip_cdata=True,
            ),
        )
        root_element = element_tree.getroot()

        author_name = (
            None
            if (author_element := root_element.find("author")) is None
            else author_element.get("name")
        )

        files_element = root_element.find("files")
        if files_element is None:
            raise Exception("Required element <files> not found.")

        files = list(
            map(
                lambda file_element: MXIFileElement(
                    source=util.xml.get_attrib(file_element, "source"),
                    destination=util.xml.get_attrib(
                        file_element, "destination"
                    ),
                    file_type=util.xml.get_attrib(file_element, "file-type"),
                ),
                files_element.iter("file"),
            )
        )

        description = (
            None
            if (description_element := root_element.find("description"))
            is None
            else description_element.text
        )

        license_agreement = (
            None
            if (
                license_agreement_element := root_element.find(
                    "license-agreement"
                )
            )
            is None
            else license_agreement_element.text
        )

        products_element = root_element.find("products")
        if products_element is None:
            raise Exception("Required element <products> not found.")

        products = list(
            map(
                lambda product_element: ProductElement(
                    name=util.xml.get_attrib(product_element, "name"),
                    version=util.xml.get_attrib(product_element, "version"),
                    primary=util.xml.get_bool_attrib(
                        product_element, "primary"
                    ),
                ),
                products_element.iter("product"),
            )
        )

        signatures = (
            None
            if (signatures_element := root_element.find("signatures")) is None
            else signatures_element.text
        )

        ui_access = (
            None
            if (ui_access_element := root_element.find("ui-access")) is None
            else ui_access_element.text
        )

        update = (
            None
            if (update_element := root_element.find("update")) is None
            else update_element.text
        )

        return MXI(
            name=util.xml.get_attrib(root_element, "name"),
            version=util.xml.get_attrib(root_element, "version"),
            type_=util.xml.get_attrib(root_element, "type"),
            requires_restart=util.xml.get_bool_attrib(
                root_element, "requires-restart"
            ),
            locked=util.xml.get_bool_attrib(root_element, "locked"),
            author=author_name,
            description=description,
            files=files,
            license_agreement=license_agreement,
            products=products,
            signatures=signatures,
            ui_access=ui_access,
            update=update,
        )

    def dump(self) -> etree._Element:
        root_element = super().dump()

        if not self.files:
            raise Exception("Atleast one FileData is required.")

        files_element = etree.SubElement(root_element, "files")
        for file in self.files:
            file_element_data = file.dump()
            etree.SubElement(
                files_element,
                file_element_data["tag"],
                file_element_data["attrib"],
            )

        return root_element
