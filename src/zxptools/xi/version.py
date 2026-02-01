__all__ = ("XIVersion",)

from typing import Any

import attrs


def alnum_vaildator(_: Any, __: Any, value: str | None) -> None:
    if value is not None and not value.isalnum():
        raise ValueError(f'"{value}" is not alphanumberic.')


@attrs.define(frozen=True)
class XIVersion:
    major: int = attrs.field(validator=attrs.validators.ge(0))
    minor: int | None = attrs.field(
        default=None, validator=attrs.validators.ge(0)
    )
    build: int | None = attrs.field(
        default=None, validator=attrs.validators.ge(0)
    )
    misc: str | None = attrs.field(default=None, validator=alnum_vaildator)

    @classmethod
    def from_str(cls, s: str) -> "XIVersion":
        split = s.split(".", maxsplit=4)

        major = int(split[0])

        minor = None
        if len(split) >= 2:
            minor = int(split[1])

        build = None
        if len(split) >= 3:
            build = int(split[2])

        misc = None
        if len(split) >= 4:
            misc = split[3]

        return cls(major, minor, build, misc)

    def __str__(self) -> str:
        return ".".join(
            map(
                str,
                filter(
                    lambda a: a is not None,
                    (
                        self.major,
                        self.minor,
                        self.build,
                        self.misc,
                    ),
                ),
            )
        )
