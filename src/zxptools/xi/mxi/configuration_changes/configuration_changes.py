__all__ = ("MXIConfigurationChanges",)

import attrs

from zxptools.xi.mxi.configuration_changes.shortcut_insert import (
    MXIShortcutInsert,
)


@attrs.define
class MXIConfigurationChanges:
    """
    Top-level container for elements that define changes to the \
    menus, shortcuts, server behaviors or formats, or data sources.
    """

    shortcut_insert: MXIShortcutInsert
