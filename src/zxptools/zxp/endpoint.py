__all__ = (
    "AbstractZxpFileEndpoint",
    "AbstractZxpFileDataEndpoint",
    "AbstractZxpSourceFileEndpoint",
    "ZxpFileEndpoint",
    "ZxpFileDataEndpoint",
    "zxp_write",
)

import os
import pathlib
import zipfile
from typing import Protocol, runtime_checkable

from zxptools.type import SizedBuffer

FileData = SizedBuffer | str


class AbstractZxpFileEndpoint(Protocol):
    def get_arcname(self) -> pathlib.PurePath: ...
    def get_destination_dirname(self) -> pathlib.PurePath: ...


@runtime_checkable
class AbstractZxpFileDataEndpoint(AbstractZxpFileEndpoint, Protocol):
    def get_data(self) -> FileData: ...


@runtime_checkable
class AbstractZxpSourceFileEndpoint(AbstractZxpFileEndpoint, Protocol):
    def get_source(self) -> pathlib.PurePath: ...


class ZxpFileEndpoint(AbstractZxpSourceFileEndpoint):
    """Indicates the start and end points of a file."""

    __slots__ = (
        "arcname",
        "destination_dir",
        "source",
    )

    def __init__(
        self,
        *,
        source: pathlib.PurePath,
        destination_dir: pathlib.PurePath,
        arcname: pathlib.PurePath | None = None,
    ) -> None:
        """
        :param source: Location of the current file.
        :param destination_dir: Directory location after the extension installation in the Flash/Animate app.
        It should start with `"$flash"`.
        :param arcname: New file name to give to file when compressed to extension file.
        """

        self.source = source

        if not os.path.isfile(self.source):
            raise Exception(f'self.source "{self.source}" is not a file.')

        self.destination_dir = destination_dir

        self.arcname = arcname

        if self.arcname is not None and self.arcname.is_absolute():
            raise Exception(
                f'self.arcname "{self.arcname}" must be a reletive path or None.'
            )

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


class ZxpFileDataEndpoint(AbstractZxpFileDataEndpoint):
    __slots__ = (
        "arcname",
        "data",
        "destination_dir",
    )

    def __init__(
        self,
        data: FileData,
        destination_dir: pathlib.PurePath,
        arcname: pathlib.PurePath,
    ) -> None:
        """
        :param data: Data to be compressed to extension file.
        :param destination_dir: Folder location after the extension installation in the Flash/Animate app.
        It should start with `"$flash"`.
        :param arcname: New file name to give to file when compressed to extension file.
        """

        self.data = data
        self.destination_dir = destination_dir
        self.arcname = arcname

    def get_arcname(self) -> pathlib.PurePath:
        return self.arcname

    def get_data(self) -> FileData:
        return self.data

    def get_destination_dirname(self) -> pathlib.PurePath:
        return self.destination_dir


def zxp_write(zxpfile: zipfile.ZipFile, file: AbstractZxpFileEndpoint) -> None:
    if isinstance(file, AbstractZxpFileDataEndpoint):
        zxpfile.writestr(file.get_arcname().as_posix(), file.get_data())
    elif isinstance(file, AbstractZxpSourceFileEndpoint):
        zxpfile.write(file.get_source(), file.get_arcname())
