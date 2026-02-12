__all__ = ("MXIBuilder",)

import xmltodict

from zxptools.exman import ExManVersion
from zxptools.type import XMLDict
from zxptools.xi.mxi.file import AbstractMXIDataFlow
from zxptools.xi.mxi.mxi import MXI
from zxptools.xi.mxi.product import MXIProduct


class MXIBuilder:
    __slots__ = (
        "exman_version",
        "extension_info",
    )

    def __init__(
        self, *, exman_version: ExManVersion = ExManVersion.CS6_OR_LATER
    ) -> None:
        self.exman_version: ExManVersion = exman_version

    def build(self, extension_info: MXI) -> str:
        self.extension_info: MXI = extension_info

        return xmltodict.unparse(
            {
                "macromedia-extension": self._get_root_element_attributes()
                | (
                    self._get_author_element()
                    | self._get_description_element()
                    | self._get_files_element()
                    | self._get_license_agreement_element()
                    | self._get_products_element()
                    | self._get_ui_access_element()
                    | self._get_update_element()
                )
            }
        )

    def _get_root_element_attributes(self) -> dict[str, str]:
        attributes: dict[str, str] = {
            "@name": self.extension_info.name,
            "@version": str(self.extension_info.version),
        }

        if (extension_type := self.extension_info.extension_type) is not None:
            attributes["@type"] = extension_type

        if (
            self.exman_version.value > ExManVersion.CS4.value
            and (icon := self.extension_info.icon) is not None
        ):
            attributes["@icon"] = icon.as_posix()

        if (
            requires_restart := self.extension_info.requires_restart
        ) is not None:
            attributes["@requires-restart"] = (
                "true" if requires_restart else "false"
            )

        return attributes

    def _get_author_element(self) -> XMLDict:
        return {"author": {"@name": self.extension_info.name}}

    def _get_description_element(self) -> XMLDict:
        if (description := self.extension_info.description) is None:
            return {}

        return {"description": {"#text": description.strip()}}

    def _get_files_element(self) -> XMLDict:
        if not self.extension_info.data_flow:
            return {}

        return {
            "files": {
                "file": tuple(
                    map(
                        self._get_file_element_attributes,
                        self.extension_info.data_flow,
                    )
                )
            }
        }

    def _get_file_element_attributes(
        self, file: AbstractMXIDataFlow
    ) -> dict[str, str]:
        attributes: dict[str, str] = {
            "@source": file.arcname.as_posix(),
            "@destination": file.destination_dir.as_posix(),
        }

        if self.exman_version.value >= ExManVersion.CS5.value:
            attributes["@file-type"] = file.file_type

        if file.platform is not None:
            attributes["@platform"] = file.platform

        if file.shared:
            attributes["@shared"] = "true"

        if file.win_extension is not None:
            attributes["@win-extension"] = file.win_extension

        return attributes

    def _get_license_agreement_element(self) -> XMLDict:
        if (
            license_agreement := self.extension_info.license_agreement
        ) is None:
            return {}

        return {"license-agreement": {"#text": license_agreement.strip()}}

    def _get_products_element(self) -> XMLDict:
        return {
            "products": {
                "product": tuple(
                    map(
                        self._get_product_element_attributes,
                        self.extension_info.products,
                    )
                )
            }
        }

    def _get_product_element_attributes(
        self, product: MXIProduct
    ) -> dict[str, str]:
        attributes: dict[str, str] = {
            "@name": product.name,
            "@version": str(product.version),
        }

        if product.primary is not None:
            attributes["@primary"] = "true" if product.primary else "false"

        if product.required is not None:
            attributes["@required"] = "true" if product.required else "false"

        return attributes

    def _get_ui_access_element(self) -> XMLDict:
        if (ui_access := self.extension_info.ui_access) is None:
            return {}

        return {"ui_access": {"#text": ui_access.strip()}}

    def _get_update_element(self) -> XMLDict:
        if (
            self.exman_version.value < ExManVersion.CS5.value
            or (update := self.extension_info.update) is None
        ):
            return {}

        return {
            "update": {
                "@url": update.url,
                "@method": update.method,
            }
        }
