__all__ = ("BaseExtensionInfo",)

from collections.abc import MutableSequence
from typing import IO, Literal

from lxml import etree

from zxptools import util
from zxptools.extension.data.base.product_xml_element_data import (
    ProductElement,
)
from zxptools.type import StrOrBytesPath


class BaseExtensionInfo:
    __slots__ = (
        "name",
        "version",
        "type",
        "requires_restart",
        "locked",
        "author",
        "products",
        "update",
        "description",
        "ui_access",
        "license_agreement",
        "signatures",
    )

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
        self.license_agreement = license_agreement
        self.products: MutableSequence[ProductElement] = (
            products if products is not None else []
        )
        self.signatures = signatures
        self.ui_access = ui_access
        self.update = update

    @classmethod
    def load(
        cls, source: StrOrBytesPath | IO[str] | IO[bytes]
    ) -> "BaseExtensionInfo":
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

        return BaseExtensionInfo(
            name=util.xml.get_attrib(root_element, "name"),
            version=util.xml.get_attrib(root_element, "version"),
            type_=util.xml.get_attrib(root_element, "type"),
            requires_restart=util.xml.get_bool_attrib(
                root_element, "requires-restart"
            ),
            locked=util.xml.get_bool_attrib(root_element, "locked"),
            author=author_name,
            description=description,
            license_agreement=license_agreement,
            products=products,
            signatures=signatures,
            ui_access=ui_access,
            update=update,
        )

    def dump(self) -> etree._Element:
        root_element = etree.Element(
            "macromedia-extension",
            {
                "name": self.name,
                "version": self.version,
                "type": self.type,
                "requires-restart": "true"
                if self.requires_restart
                else "false",
                "locked": "true" if self.locked else "false",
            },
        )

        if self.author is not None:
            etree.SubElement(root_element, "author", {"name": self.author})

        if not self.products:
            raise Exception(
                "Atleast one ProductData in MXI.products is required."
            )

        products_element = etree.SubElement(root_element, "products")
        for product in self.products:
            product_element_data = product.dump()
            etree.SubElement(
                products_element,
                product_element_data["tag"],
                product_element_data["attrib"],
            )

        if self.update is not None:
            update_element = etree.SubElement(root_element, "update")
            update_element.text = etree.CDATA(self.update)

        if self.description is not None:
            update_element = etree.SubElement(root_element, "description")
            update_element.text = etree.CDATA(self.description)

        if self.ui_access is not None:
            ui_access_element = etree.SubElement(root_element, "ui-access")
            ui_access_element.text = etree.CDATA(self.ui_access)

        if self.license_agreement is not None:
            license_agreement_element = etree.SubElement(
                root_element, "license-agreement"
            )
            license_agreement_element.text = etree.CDATA(
                self.license_agreement
            )

        if self.signatures is not None:
            signatures_element = etree.SubElement(root_element, "signatures")
            signatures_element.text = etree.CDATA(self.signatures)

        return root_element
