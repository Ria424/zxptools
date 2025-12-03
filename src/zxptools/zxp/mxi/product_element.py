__all__ = ("ProductElement",)


class ProductElement:
    __slots__ = (
        "name",
        "primary",
        "version",
    )

    def __init__(self, *, name: str, version: str, primary: bool) -> None:
        self.name = name
        self.version = version
        self.primary = primary

    def dump(self) -> dict[str, str]:
        return {
            "name": self.name,
            "version": self.version,
            "primary": "true" if self.primary else "false",
        }
