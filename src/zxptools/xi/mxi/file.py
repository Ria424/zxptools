__all__ = ("MXIFile",)

import os
import pathlib
import attrs


def _validate_source(source: pathlib.PurePath) -> None:
    if not os.path.isfile(source):
        raise ValueError(f'source "{source}" is not a file.')

    # if source.is_absolute():
    #     raise ValueError(
    #         "source must be a relative path inside the extension."
    #     )


def _validate_arcname(arcname: pathlib.PurePath | None) -> None:
    if arcname is not None and arcname.is_absolute():
        raise ValueError(
            f'arcname "{arcname}" must be a reletive path or None.'
        )


@attrs.define(frozen=True)
class MXIFile:
    """Indicates the start and end points of a file."""

    source: pathlib.PurePath = attrs.field(
        validator=lambda _, __, value: _validate_source(value)
    )
    """Location of the current file."""

    destination_dir: pathlib.PurePath
    """Directory location after the extension installation in the Flash/Animate app."""

    arcname: pathlib.PurePath | None = attrs.field(
        default=None, validator=lambda _, __, value: _validate_arcname(value)
    )
    """New file name to give to file when compressed to extension file."""

    def get_arcname(self) -> pathlib.PurePath:
        return (
            self.arcname
            if self.arcname is not None
            else pathlib.PurePath(os.path.relpath(self.source, os.getcwd()))
        )

    def get_source(self) -> pathlib.PurePath:
        return self.source

    def get_destination_dirname(self) -> pathlib.PurePath:
        return self.destination_dir
