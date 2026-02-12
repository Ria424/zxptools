__all__ = (
    "FireworksExtensionType",
    "FIREWORKS_EXTENSION_TYPE",
    "is_valid_fireworks_extension_type",
)

from typing import Literal, TypeGuard, Final

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

FIREWORKS_EXTENSION_TYPE: Final[tuple[FireworksExtensionType, ...]] = (
    "autoshape",
    "command",
    "commandpanel",
    "dictionary",
    "keyboard shortcut",
    "library",
    "pattern",
    "texture",
)


def is_valid_fireworks_extension_type(
    extension_type: str,
) -> TypeGuard[FireworksExtensionType]:
    return extension_type in FIREWORKS_EXTENSION_TYPE
