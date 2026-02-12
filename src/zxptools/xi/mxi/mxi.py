__all__ = ("MXI",)

import pathlib
from collections.abc import MutableSequence
from typing import Any

import attrs

from zxptools.xi.mxi import extension_type
from zxptools.xi.mxi.file import AbstractMXIDataFlow
from zxptools.xi.mxi.product import MXIProduct
from zxptools.xi.mxi.update import MXIUpdate
from zxptools.xi.version import XIVersion


def attrs_extension_type_validator(
    inst: Any, attr: attrs.Attribute, value: Any
) -> None:
    if not extension_type.is_valid_extension_type(value):
        raise ValueError(
            f"'{attr.name}' is not valid extension type: \"{value}\""
        )


@attrs.define(frozen=True, kw_only=True)
class MXI:
    name: str = attrs.field(validator=attrs.validators.max_len(255))
    """
    The name of the extension with a limit of 255 characters, displayed in Extension Manager.
    """

    version: XIVersion
    """The version number of the latest version of the extension."""

    products: MutableSequence[MXIProduct]
    """
    A container for one or more product elements, \
    each of which specifies an Adobe product in which this extension can be installed.
    """

    extension_type: extension_type.ExtensionType = attrs.field(
        default=None, validator=attrs_extension_type_validator
    )
    """
    Dreamweaver, Fireworks, and Flash only.
    The type of this extension. Values are case-insensitive.
    """

    icon: pathlib.PurePath | None = None
    """
    The path to a customized icon for this extension, to display in Extension Manager.

    In order for a custom icon to be displayed, \
    the icon file must be installed in the folder specified by ``$ExtensionSpecificEMStore``.

    For example:

    ```
    <file source="myIcon.png" destination="$ExtensionSpecificEMStore" />
    ```

    Icons are only shown in application versions CS4 and later.
    For CS3 or earlier, use the ``extension_type`` attribute.
    If not specified, a default icon is used.
    """

    requires_restart: bool = False
    """
    Whether the target product must be restarted after the extension is installed.

    Default is ``False``.
    """

    show_files: bool = True
    """
    (CS5 or later)

    Whether the Advanced tab in the Extension Manager \
    displays path information for all files where this extension is installed.

    Default is ``True``.
    """

    author: str | None = attrs.field(
        default=None,
        validator=attrs.validators.optional(attrs.validators.max_len(255)),
    )
    """Name of the extension's author with a limit of 255 characters."""

    data_flow: MutableSequence[AbstractMXIDataFlow] = attrs.field(factory=list)
    """
    A container for one or more ``AbstractMXIEndpoint``s \
    that describe specific *file or file contents* to be installed as part of the extension.
    """

    description: str | None = attrs.field(
        default=None,
        validator=attrs.validators.optional(attrs.validators.max_len(2000)),
    )
    """
    Contains or points to HTML text that describes what the extension does or is used for.
    The text appears in the Extension Manager when the extension is selected.
    """

    license_agreement: str | None = attrs.field(
        default=None,
        validator=attrs.validators.optional(attrs.validators.max_len(2000)),
    )
    """
    Allows a third-party developer to include a license agreement with an extension.

    If supplied, the contents of this element are displayed \
    under the heading Third Party License, \
    at the end of the Adobe new-extension installation license.
    """

    ui_access: str | None = attrs.field(
        default=None,
        validator=attrs.validators.optional(attrs.validators.max_len(512)),
    )
    """
    Contains or points to HTML text that describes the extension's user interface.

    Together with the description element, \
    determines the text that appears in the Extension Manager window \
    when the extension is selected.

    You should include information about where to find the item \
    in the product's user interface, \
    as well as a brief description of the item's use.
    """

    update: MXIUpdate | None = None
    """
    (CS5 or later)
    Provides update information for extension.

    If supplied, Extension Manager checks the given site for updates, \
    and when an update is available, prompts the user to update the extension.
    """
