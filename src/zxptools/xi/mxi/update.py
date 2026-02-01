__all__ = (
    "MXIUpdate",
    "MXIUpdateMethod",
)

from typing import Literal

import attrs

MXIUpdateMethod = Literal["directlink"]


@attrs.define
class MXIUpdate:
    url: str
    method: MXIUpdateMethod = "directlink"
