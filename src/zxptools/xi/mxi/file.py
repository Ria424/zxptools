__all__ = (
    "AbstractMXIDataFlow",
    "AbstractMXIFile",
    "AbstractMXIFileData",
    "FileType",
    "MXIFile",
    "MXIFileData",
    "is_valid_file_type",
)

import os
import pathlib
from abc import ABC
from collections.abc import Sequence
from typing import Any, Literal, TypeGuard

import attrs

from zxptools import util
from zxptools.type import SizedBuffer


def attrs_source_validator(
    inst: Any, attr: attrs.Attribute, value: Any
) -> None:
    if not os.path.isfile(value):
        raise ValueError(f"'{attr.name}' must be a file: \"{value}\"")


FileType = Literal["csxs", "plugin", "ordinary"]


def is_valid_file_type(file_type: Any) -> TypeGuard[FileType]:
    return (
        file_type == "ordinary" or file_type == "plugin" or file_type == "csxs"
    )


def attrs_file_type_validator(
    _: Any, attr: attrs.Attribute, value: Any
) -> None:
    if is_valid_file_type(value):
        raise ValueError(
            f'\'{attr.name}\' must be "csxs", "plugin" or "ordinary": {value}'
        )


class AbstractMXIDataFlow(ABC):
    destination_dir: pathlib.PurePath
    arcname: pathlib.PurePath
    platform: Literal["mac", "win"] | None
    shared: bool
    win_extension: str | None
    file_type: FileType
    dependencies: Sequence[pathlib.PurePath]


class AbstractMXIFile(AbstractMXIDataFlow, ABC):
    source: pathlib.PurePath


class AbstractMXIFileData(AbstractMXIDataFlow, ABC):
    data: SizedBuffer


@attrs.define
class _MXIFileMetadata:
    platform: Literal["mac", "win"] | None = None
    """
    What platform the file is intended for.

    If you specify a platform, the file is installed only on that platform; for instance, \
    you can provide two versions of a file,
    one for Windows and one for Macintosh, and specify a platform value for each.
    If it's ``None``, the file is installed on both platforms.
    """

    shared: bool = False
    """
    Whether the file is used by more than one extension.
    When you use the Extension Manager to remove an extension, \
    a shared file associated with that extension is not deleted \
    as long as other installed extensions refer to that file.
    """

    win_extension: str | None = None
    """
    A file-name extension to use when a file generated in Mac OS \
    that does not include the Windows extension, such as ``.fla`` or ``.htm``.
    If you create a file on Windows that does include the extension, such as "mypage.htm",
    and install it in Mac OS, this value is not needed.
    If a platform attribute value is supplied, this attribute is ignored.
    """

    file_type: FileType = attrs.field(validator=attrs_file_type_validator)
    """
    (CS5 or later)

    - ``csxs``: A CS extension package.
    - ``ordinary``: Ordinary files receive no special processing by Extension Manager.
    - ``plugin``: A native plug-in.
    """


@attrs.define(frozen=True)
class MXIFile(_MXIFileMetadata, AbstractMXIFile):
    """Indicates the start and end points of a file."""

    source: pathlib.PurePath = attrs.field(validator=attrs_source_validator)
    """Location of the current file."""

    destination_dir: pathlib.PurePath
    """Directory location after the extension installation in the Flash/Animate app."""

    arcname: pathlib.PurePath = attrs.field(
        default=attrs.Factory(
            lambda self: pathlib.PurePath(
                os.path.relpath(self.source, os.getcwd())
            ),
            takes_self=True,
        ),
        validator=util.attrs.validators.relative_path(),
    )
    """New file name to give to file when compressed to extension file."""

    @property
    def dependencies(self) -> tuple[pathlib.PurePath, ...]:
        """Which file should be changed to update the Watch file?"""
        return (self.source,)


@attrs.define(frozen=True)
class MXIFileData(_MXIFileMetadata, AbstractMXIFileData):
    data: SizedBuffer
    """File contents."""

    destination_dir: pathlib.PurePath
    """Directory location after the extension installation in the Flash/Animate app."""

    arcname: pathlib.PurePath = attrs.field(
        validator=util.attrs.validators.relative_path()
    )
    """File name to give to file when compressed to extension file."""

    dependencies: Sequence[pathlib.PurePath] = attrs.field(factory=list)
    """Which file should be changed to update the Watch file?"""


@attrs.define(frozen=False)
class MutableMXIFileData(MXIFileData):
    pass
