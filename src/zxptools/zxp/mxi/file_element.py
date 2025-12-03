__all__ = ("FileElement",)

from typing import Literal


class FileElement:
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

    def dump(self) -> dict[str, str]:
        return {
            "source": self.source,
            "destination": self.destination,
            "file_type": self.file_type,
        }
