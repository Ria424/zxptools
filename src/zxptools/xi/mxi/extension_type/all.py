__all__ = (
    "ExtensionType",
    "is_valid_extension_type",
)

from typing import TypeGuard, Union

from zxptools.xi.mxi.extension_type.dreamweaver import (
    DreamweaverExtensionType,
    is_valid_dreamweaver_extension_type,
)
from zxptools.xi.mxi.extension_type.fireworks import (
    FireworksExtensionType,
    is_valid_fireworks_extension_type,
)
from zxptools.xi.mxi.extension_type.flash import (
    FlashExtensionType,
    is_valid_flash_extension_type,
)

ExtensionType = Union[
    DreamweaverExtensionType, FireworksExtensionType, FlashExtensionType
]


def is_valid_extension_type(extension_type: str) -> TypeGuard[ExtensionType]:
    return (
        is_valid_dreamweaver_extension_type(extension_type)
        or is_valid_fireworks_extension_type(extension_type)
        or is_valid_flash_extension_type(extension_type)
    )
