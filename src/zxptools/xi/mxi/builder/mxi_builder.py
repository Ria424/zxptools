__all__ = ("MXIBuilder",)

from typing import Any

import xmltodict

from zxptools.type import XMLMutableMapping
from zxptools.xi.mxi.file import MXIFile
from zxptools.xi.mxi.mxi import MXI
from zxptools.xi.mxi.product import MXIProduct


class MXIBuilder:
    __slots__ = ("extension_info",)

    def build(self, extension_info: MXI) -> str:
        self.extension_info = extension_info

        xmldict = self._get_root_element()
        xmldict_children = {}
        xmldict_children.update(self._get_author_element())
        xmldict_children.update(self._get_description_element())
        xmldict_children.update(self._get_files_element())
        xmldict_children.update(self._get_license_agreement_element())
        xmldict_children.update(self._get_products_element())
        xmldict_children.update(self._get_ui_access_element())
        xmldict_children.update(self._get_update_element())
        xmldict["macromedia-extension"].update(xmldict_children)
        return xmltodict.unparse(xmldict)

    def _get_root_element(self) -> XMLMutableMapping:
        root_element_attrib: dict[str, str] = {
            "@name": self.extension_info.name,
            "@version": str(self.extension_info.version),
        }

        if self.extension_info.extension_type is not None:
            root_element_attrib["@type"] = self.extension_info.extension_type

        if self.extension_info.requires_restart is not None:
            root_element_attrib["@requires-restart"] = (
                "true" if self.extension_info.requires_restart else "false"
            )

        return {"macromedia-extension": root_element_attrib}

    def _get_author_element(self) -> XMLMutableMapping:
        return {"author": {"@name": self.extension_info.name}}

    def _get_description_element(self) -> XMLMutableMapping:
        if self.extension_info.description is None:
            return {}
        return {"description": self.extension_info.description}

    def _get_files_element(self) -> XMLMutableMapping:
        if self.extension_info.files is None:
            return {}
        return {
            "files": {
                "file": tuple(
                    map(self._get_file_element, self.extension_info.files)
                )
            }
        }

    def _get_file_element(self, file: MXIFile) -> XMLMutableMapping:
        return {
            "@source": file.arcname,
            "@destination": file.destination_dir,
            "@file-type": "ordinary",
        }

    def _get_license_agreement_element(self) -> XMLMutableMapping:
        if self.extension_info.license_agreement is None:
            return {}
        return {"license-agreement": self.extension_info.license_agreement}

    def _get_products_element(self) -> XMLMutableMapping:
        return {
            "products": {
                "product": tuple(
                    map(
                        self._get_product_element, self.extension_info.products
                    )
                )
            }
        }

    def _get_product_element(self, product: MXIProduct) -> XMLMutableMapping:
        attrib: dict[str, Any] = {
            "@name": product.name,
            "@version": product.version,
        }
        if product.primary is not None:
            attrib["@primary"] = "true" if product.primary else "false"
        if product.required is not None:
            attrib["@required"] = "true" if product.required else "false"
        return attrib

    def _get_ui_access_element(self) -> XMLMutableMapping:
        if self.extension_info.ui_access is None:
            return {}
        return {"ui_access": self.extension_info.ui_access}

    def _get_update_element(self) -> XMLMutableMapping:
        if self.extension_info.update is None:
            return {}
        return {
            "update": {
                "@url": self.extension_info.update.url,
                "@method": self.extension_info.update.method,
            }
        }
