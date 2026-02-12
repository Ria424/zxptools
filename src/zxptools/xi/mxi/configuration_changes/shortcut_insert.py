__all__ = (
    "MXIShortcutInsert",
    "MXIShortcutList",
    "MXIShortcut",
    "MXIShortcutBehavior",
    "MXICommandShortcut",
    "MXIFileShortcut",
)

import pathlib
from typing import Any, Literal

import attrs


@attrs.define
class MXIShortcutInsert:
    """
    Container for elements that describe additions to the shortcuts in the menus.xml file.
    """

    list_id: str
    """
    The unique identifier of a shortcut list in which to add the contained ``<shortcut>`` element.
    Required for this case; do not use if this element contains a ``<shortcutlist>`` element.
    """

    shortcut: "MXIShortcutList | MXIShortcut"


@attrs.define
class MXIShortcutList:
    """A shortcut list to add to the menus.xml file."""

    id: str
    """
    The unique identifier of the shortcut list,
    which matches the Dreamweaver window containing the menubar with which the shortcuts are associated.
    One of ``DWMainWindow``, ``DWMainSite``, ``DWTimelineInspector``, and ``DWHTMLInspector``.
    """

    platform: Literal["mac", "win"] | None = None
    """
    The platform in which this list appears, one of "mac" or "win".
    If not specified, the list appears on both platforms.
    """


@attrs.define
class MXIShortcut:
    """
    A keyboard shortcut to add to the menus.xml file.
    The JavaScript to execute when the shortcut is activated can be contained directly in the command attribute,
    or in a specified file. One of these must be supplied; if both are supplied, the file takes precedence.
    """

    key: str
    """
    The key combination used to activate the associated command.
    Use the syntax specified for keyboard shortcuts in Dreamweaver documentation.
    For example: ``Shift+F5``
    """

    id: str
    """
    A unique identifier for the new shortcut. Each ID must be unique;
    it should start with a company name or other unique namespace prefix.
    Do not use DW as a prefix; it is reserved by the Dreamweaver.
    A convention is to use a domain name with the elements reversed; for example, ``com.adobe``.
    """

    behavior: "MXICommandShortcut | MXIFileShortcut"

    command: str | None = None
    """If not supplied, file is required. JavaScript code to execute when the command is activated."""

    file: str | None = None
    """
    if not supplied, command is required.
    A file containing JavaScript code to execute when the command is activated.
    """

    platform: Literal["mac", "win"] | None = None
    """
    The platform in which this shortcut appears, one of "mac" or "win".
    If not specified, the shortcut appears on both platforms.
    """


@attrs.define
class MXIShortcutBehavior:
    """
    Used in ``MXIShortcut``.
    """

    type: Literal["command", "file"]
    value: Any


@attrs.define
class MXICommandShortcut(MXIShortcutBehavior):
    """
    Varient of ``MXIShortcutBehavior``.
    """

    type: Literal["command"] = "command"
    value: str


@attrs.define
class MXIFileShortcut(MXIShortcutBehavior):
    """
    Varient of ``MXIShortcutBehavior``.
    """

    type: Literal["file"] = "file"
    value: pathlib.PurePath
