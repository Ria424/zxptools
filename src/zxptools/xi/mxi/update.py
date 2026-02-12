__all__ = (
    "MXIUpdate",
    "MXIUpdateMethod",
)

from typing import Literal

import attrs

MXIUpdateMethod = Literal["directlink"]


@attrs.define
class MXIUpdate:
    """
    Provides update information for extension.
    """

    url: str
    """
    A URL for an extension update information file.
    
    The value must start with either ``"http://"`` or ``"https://"``.
    """

    method: MXIUpdateMethod = "directlink"
    """
    Reserved for future use in identifying an update-checking method.
    
    The only currently supported value is the default, directlink.
    """
