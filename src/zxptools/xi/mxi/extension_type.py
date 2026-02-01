__all__ = (
    "DreamweaverExtensionType",
    "FireworksExtensionType",
    "FlashExtensionType",
)

from typing import Literal

DreamweaverExtensionType: Literal[
    "behavior",
    "browserprofile",
    "codehint codesnippet",
    "coloringscheme",
    "command",
    "connection",
    "datasource",
    "dictionary",
    "documenttype",
    "encoding",
    "flashbuttonstyle",
    "flashelement",
    "floater",
    "insertbar",
    "jsextension",
    "keyboard shortcut",
    "object",
    "plugin",
    "propertyinspector",
    "report",
    "referencebook",
    "samplecontent",
    "serverbehavior",
    "serverformat",
    "servermodel",
    "site",
    "suite",
    "taglibrary",
    "template",
    "thirdpartytags",
    "toolbar",
    "translator",
    "utility",
    "query",
]

FireworksExtensionType = Literal[
    "autoshape",
    "command",
    "commandpanel",
    "dictionary",
    "keyboard shortcut",
    "library",
    "pattern",
    "texture",
]

FlashExtensionType = Literal[
    "actionscript",
    "flashcomponent",
    "flashcustomaction",
    "flashimporter",
    "flashpanel",
    "flashtemplate",
    "keyboardshortcut",
    "lesson",
    "library",
    "publishtemplate",
    "sample",
    "smartclip",
    "utility",
    "generatorobject",  # Flash 5 or earlier
]
