__all__ = ("XIVersion",)

from typing import Any

import attrs


def alnum_validator(
    _: Any, attribute: attrs.Attribute, value: str | None
) -> None:
    if value is not None and not value.isalnum():
        raise ValueError(f"{attribute.name} must be alphanumberic: {value}")


def version_num_validator(
    _: Any, attribute: attrs.Attribute, value: int | None
) -> None:
    if value is not None and value < 0:
        raise ValueError(
            f"{attribute.name} must be a non-negative integer: {value}"
        )


@attrs.define(frozen=True)
class XIVersion:
    """major[.minor[.build[.misc]]]"""

    major: int = attrs.field(validator=version_num_validator)
    minor: int | None = attrs.field(
        default=None, validator=version_num_validator
    )
    build: int | None = attrs.field(
        default=None, validator=version_num_validator
    )
    misc: str | None = attrs.field(default=None, validator=alnum_validator)

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

    def __eq__(self, value: Any) -> bool:
        return (
            self.major == value.major
            and self.minor == value.minor
            and self.build == value.build
            and self.misc == value.misc
        )

    def __ne__(self, value: Any) -> bool:
        return (
            self.major != value.major
            or self.minor != value.minor
            or self.build != value.build
            or self.misc != value.misc
        )

    def __lt__(self, value: Any) -> bool:
        return self.to_tuple() < XIVersion.to_tuple(value)

    def __le__(self, value: Any) -> bool:
        return self.to_tuple() <= XIVersion.to_tuple(value)

    def __gt__(self, value: Any) -> bool:
        return self.to_tuple() > XIVersion.to_tuple(value)

    def __ge__(self, value: Any) -> bool:
        return self.to_tuple() >= XIVersion.to_tuple(value)

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

    def to_tuple(
        self,
    ) -> (
        tuple[int]
        | tuple[int, int]
        | tuple[int, int, int]
        | tuple[int, int, int, str]
    ):
        return tuple(
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


@attrs.define(frozen=True)
class XIMiniVersion:
    """
    Shorter version of ``XIMiniVersion``
    major[.minor[.build]]
    """

    major: int = attrs.field(validator=version_num_validator)
    minor: int | None = attrs.field(
        default=None, validator=version_num_validator
    )
    build: int | None = attrs.field(
        default=None, validator=version_num_validator
    )

    @classmethod
    def from_str(cls, s: str) -> "XIMiniVersion":
        split = s.split(".", maxsplit=4)

        major = int(split[0])

        minor = None
        if len(split) >= 2:
            minor = int(split[1])

        build = None
        if len(split) >= 3:
            build = int(split[2])

        return cls(major, minor, build)

    def __eq__(self, value: Any) -> bool:
        return (
            self.major == value.major
            and self.minor == value.minor
            and self.build == value.build
        )

    def __ne__(self, value: Any) -> bool:
        return (
            self.major != value.major
            or self.minor != value.minor
            or self.build != value.build
        )

    def __lt__(self, value: Any) -> bool:
        return self.to_tuple() < XIVersion.to_tuple(value)

    def __le__(self, value: Any) -> bool:
        return self.to_tuple() <= XIVersion.to_tuple(value)

    def __gt__(self, value: Any) -> bool:
        return self.to_tuple() > XIVersion.to_tuple(value)

    def __ge__(self, value: Any) -> bool:
        return self.to_tuple() >= XIVersion.to_tuple(value)

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
                    ),
                ),
            )
        )

    def to_tuple(
        self,
    ) -> (
        tuple[int]
        | tuple[int, int]
        | tuple[int, int, int]
        | tuple[int, int, int, str]
    ):
        return tuple(
            filter(
                lambda a: a is not None,
                (
                    self.major,
                    self.minor,
                    self.build,
                ),
            ),
        )
