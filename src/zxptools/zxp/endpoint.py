__all__ = (
    "AbstractZxpFileEndpoint",
    "AbstractZxpFileDataEndpoint",
    "AbstractZxpSourceFileEndpoint",
    "ZxpStandardFileEndpoint",
    "ZxpArcFileEndpoint",
    "ZxpFileEndpoint",
    "ZxpFileDataEndpoint",
    "zxp_write",
)

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


class ZxpStandardFileEndpoint(AbstractZxpSourceFileEndpoint):
    __slots__ = (
        "source",
        "destination_dirname",
    )

    def __init__(
        self, source: pathlib.PurePath, destination_dirname: pathlib.PurePath
    ) -> None:
        self.source = source
        self.destination_dirname = destination_dirname

    def get_arcname(self) -> pathlib.PurePath:
        return self.source

    def get_source(self) -> pathlib.PurePath:
        return self.source

    def get_destination_dirname(self) -> pathlib.PurePath:
        return self.destination_dirname


class ZxpArcFileEndpoint(AbstractZxpSourceFileEndpoint):
    __slots__ = (
        "source",
        "destination_dirname",
        "arcname",
    )

    def __init__(
        self,
        source: pathlib.PurePath,
        destination_dirname: pathlib.PurePath,
        arcname: pathlib.PurePath,
    ) -> None:
        self.source = source
        self.destination_dirname = destination_dirname
        self.arcname = arcname

    def get_arcname(self) -> pathlib.PurePath:
        return self.arcname

    def get_source(self) -> pathlib.PurePath:
        return self.source

    def get_destination_dirname(self) -> pathlib.PurePath:
        return self.destination_dirname


class ZxpFileEndpoint(AbstractZxpSourceFileEndpoint):
    __slots__ = (
        "source",
        "destination",
    )

    def __init__(
        self, source: pathlib.PurePath, destination: pathlib.PurePath
    ) -> None:
        self.source = source
        self.destination = destination

    def get_arcname(self) -> pathlib.PurePath:
        return self.source.parent / self.destination.name

    def get_source(self) -> pathlib.PurePath:
        return self.source

    def get_destination_dirname(self) -> pathlib.PurePath:
        return self.destination


class ZxpFileDataEndpoint(AbstractZxpFileDataEndpoint):
    __slots__ = (
        "data",
        "arcname",
        "destination",
    )

    def __init__(
        self,
        data: FileData,
        arcname: pathlib.PurePath,
        destination: pathlib.PurePath,
    ) -> None:
        self.data = data
        self.arcname = arcname
        self.destination = destination

    def get_arcname(self) -> pathlib.PurePath:
        return self.arcname

    def get_data(self) -> FileData:
        return self.data

    def get_destination_dirname(self) -> pathlib.PurePath:
        return self.destination


def zxp_write(zxpfile: zipfile.ZipFile, file: AbstractZxpFileEndpoint) -> None:
    if isinstance(file, AbstractZxpFileDataEndpoint):
        zxpfile.writestr(file.get_arcname().as_posix(), file.get_data())
    elif isinstance(file, AbstractZxpSourceFileEndpoint):
        zxpfile.write(file.get_source(), file.get_arcname())
