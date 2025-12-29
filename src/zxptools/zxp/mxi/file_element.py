__all__ = ("MXIFileElement",)

from typing import Literal

from zxptools.type import XMLElementData


class MXIFileElement:
    __slots__ = (
        "destination",
        "file_type",
        "source",
    )

    def __init__(
        self,
        *,
        source: str,
        destination: str,
        file_type: Literal["ordinary"] = "ordinary",
    ) -> None:
        self.source = source
        self.destination = destination
        self.file_type = file_type

    def dump(self) -> XMLElementData:
        return {
            "attrib": {
                "source": self.source,
                "destination": self.destination,
                "file_type": self.file_type,
            },
            "tag": "file",
            "text": None,
        }
