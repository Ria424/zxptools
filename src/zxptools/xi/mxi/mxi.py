__all__ = ("MXI",)

from collections.abc import MutableSequence

import attrs

from zxptools.xi.mxi.file import MXIFile
from zxptools.xi.mxi.product import MXIProduct
from zxptools.xi.mxi.update import MXIUpdate
from zxptools.xi.version import XIVersion


@attrs.define
class MXI:
    name: str = attrs.field(
        validator=(
            attrs.validators.min_len(1),
            attrs.validators.max_len(255),
        )
    )
    """
    The name of the extension, displayed in Extension Manager.
    A `VARCHAR` data type with a limit of 255 characters.
    """

    version: XIVersion
    """The version number of the latest version of the extension."""

    extension_type: str | None = None
    """
    Dreamweaver, Fireworks, and Flash only.
    The type of this extension. Values are case-insensitive.
    """

    requires_restart: bool | None = None
    """
    When true, the target product must be restarted after the extension is installed.
    Default is `false`.

    Superceded by force-quit, introduced in Extension Manager CS5.
    """

    author: str | None = None
    """Name of the extension's author."""

    description: str = ""
    """
    Contains or points to HTML text that describes what the extension does or is used for.
    The text appears in the Extension Manager when the extension is selected.
    """

    files: MutableSequence[MXIFile] = attrs.field(factory=list)
    """
    A container for one or more file elements
    that describe specific files to be installed as part of the extension.
    """

    license_agreement: str | None = None
    """
    Allows a third-party developer to include a license agreement with an extension.
    If supplied, the contents of this element are displayed under the heading Third Party License,
    at the end of the Adobe new-extension installation license.
    """

    products: MutableSequence[MXIProduct] = attrs.field(
        factory=lambda: [MXIProduct("Flash", "7", True)]
    )
    """
    A container for one or more product elements,
    each of which specifies an Adobe product in which this extension can be installed.
    """

    ui_access: str | None = None
    """
    Contains or points to HTML text that describes the extension's user interface.
    Together with the description element,
    determines the text that appears in the Extension Manager window when the extension is selected.
    You should include information about where to find the item in the product's user interface,
    as well as a brief description of the item's use.
    """

    update: MXIUpdate | None = None
    """
    Provides update information for this extension.
    If supplied, Extension Manager checks the given site for updates,
    and when an update is available, prompts the user to update the extension.
    """
