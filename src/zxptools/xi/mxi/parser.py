__all__ = ("MXIParser",)

import pathlib
from typing import Any, TypeGuard, Literal

from lxml import etree

from zxptools import util
from zxptools.type import StrOrBytesPath
from zxptools.xi import XIVersion
from zxptools.xi.mxi import (
    MXI,
    MXIFile,
    MXIProduct,
    MXIUpdate,
    file,
)
from zxptools.xi.mxi.file import AbstractMXIDataFlow


class MXIParser:
    def parse(self, source: StrOrBytesPath) -> MXI:
        element_tree = etree.parse(
            source,
            parser=etree.XMLParser(
                encoding="UTF-8",
                remove_blank_text=True,
                remove_comments=True,
                strip_cdata=True,
            ),
        )
        self.root_element = element_tree.getroot()

        return MXI(
            name=util.xml.get_attrib(self.root_element, "name", strict=True),
            version=XIVersion.from_str(
                util.xml.get_attrib(self.root_element, "version", strict=True)
            ),
            products=self._parse_products_element(),
            extension_type=util.xml.get_attrib(self.root_element, "type"),
            icon=(
                None
                if (
                    icon_raw_path := util.xml.get_attrib(
                        self.root_element, "icon"
                    )
                )
                is None
                else pathlib.PurePath(icon_raw_path)
            ),
            requires_restart=util.xml.get_bool_attrib(
                self.root_element, "requires-restart", default=False
            ),
            author=self._parse_author_element(),
            data_flow=self._parse_files_element(),
            description=self._parse_description_element(),
            license_agreement=self._parse_license_agreement_element(),
            update=self._parse_update_element(),
            ui_access=self._parse_ui_access_element(),
        )

    def _is_valid_platform(
        self, platform: Any
    ) -> TypeGuard[Literal["mac", "win"]]:
        return platform == "mac" or platform == "win"

    def _parse_author_element(self) -> str | None:
        return (
            None
            if (author_element := self.root_element.find("author")) is None
            else author_element.get("name")
        )

    def _parse_description_element(self) -> str:
        return (
            None
            if (description_element := self.root_element.find("description"))
            is None
            else description_element.text
        ) or ""

    def _parse_files_element(self) -> list[AbstractMXIDataFlow]:
        files_element = self.root_element.find("files")
        if files_element is None:
            return []

        return list(
            map(
                self._parse_file_element,
                files_element.iter("file"),
            )
        )

    def _parse_file_element(self, file_element: Any) -> AbstractMXIDataFlow:
        return MXIFile(
            source=pathlib.PurePath(
                util.xml.get_attrib(file_element, "source", strict=True)
            ),
            destination_dir=pathlib.PurePath(
                util.xml.get_attrib(file_element, "destination", strict=True)
            ),
            file_type=file.is_valid_file_type(
                util.xml.get_attrib(
                    file_element, "file-type", default="ordinary"
                )
            ),
            platform=self._is_valid_platform(
                util.xml.get_attrib(file_element, "platform")
            ),
            shared=(
                util.xml.get_attrib(file_element, "shared", default="")
                == "true"
            ),
            win_extension=util.xml.get_attrib(file_element, "win-extension"),
        )

    def _parse_license_agreement_element(self) -> str | None:
        return (
            None
            if (
                license_agreement_element := self.root_element.find(
                    "license-agreement"
                )
            )
            is None
            else license_agreement_element.text
        )

    def _parse_products_element(self) -> list[MXIProduct]:
        products_element = self.root_element.find("products")
        if products_element is None:
            raise Exception("Required element <products> not found.")

        return list(
            map(
                self._parse_product_element,
                products_element.iter("product"),
            )
        )

    def _parse_product_element(self, product_element: Any) -> MXIProduct:
        return MXIProduct(
            name=util.xml.get_attrib(product_element, "name", strict=True),
            version=util.xml.get_attrib(
                product_element, "version", strict=True
            ),
            primary=util.xml.get_bool_attrib(product_element, "primary"),
            required=util.xml.get_bool_attrib(product_element, "required"),
        )

    def _parse_ui_access_element(self) -> str | None:
        return (
            None
            if (ui_access_element := self.root_element.find("ui-access"))
            is None
            else ui_access_element.text
        )

    def _parse_update_element(self) -> MXIUpdate | None:
        return (
            None
            if (update_element := self.root_element.find("update")) is None
            else MXIUpdate(
                url=util.xml.get_attrib(update_element, "url", strict=True),
                method=(
                    util.xml.get_attrib(
                        update_element, "method", default="directlink"
                    )
                ),
            )
        )
