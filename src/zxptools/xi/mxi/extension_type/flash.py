__all__ = (
    "FlashExtensionType",
    "FLASH_EXTENSION_TYPE",
    "is_valid_flash_extension_type",
)

from typing import Final, TypeGuard, Literal

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

FLASH_EXTENSION_TYPE: Final[tuple[FlashExtensionType, ...]] = (
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
)


def is_valid_flash_extension_type(
    extension_type: str,
) -> TypeGuard[FlashExtensionType]:
    return extension_type in FLASH_EXTENSION_TYPE
