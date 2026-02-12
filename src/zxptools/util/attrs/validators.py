__all__ = (
    "absolute_path",
    "relative_path",
)

import os
from typing import Any

import attrs


@attrs.define(repr=False)
class _AbsolutePathValidator:
    def __call__(self, inst: Any, attr: attrs.Attribute, value: Any):
        """
        Use a callable class to be able to change the ``__repr__``.
        """

        if not os.path.isabs(value):
            raise ValueError(
                f"'{attr.name}' must be an absolute path: {value}"
            )

    def __repr__(self) -> str:
        return "<absolute_path validator>"


def absolute_path() -> _AbsolutePathValidator:
    return _AbsolutePathValidator()


@attrs.define(repr=False)
class _RelativePathValidator:
    def __call__(self, inst: Any, attr: attrs.Attribute, value: Any):
        """
        Use a callable class to be able to change the ``__repr__``.
        """

        if os.path.isabs(value):
            raise ValueError(
                f"'{attr.name}' must be an relative path: {value}"
            )

    def __repr__(self) -> str:
        return "<relative_path validator>"


def relative_path() -> _RelativePathValidator:
    return _RelativePathValidator()
