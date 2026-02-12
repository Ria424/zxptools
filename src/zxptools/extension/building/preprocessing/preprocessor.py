import os
import pathlib
import warnings
from collections.abc import Generator, Iterable, Sequence
from typing import Protocol

from zxptools.type import StrOrBytesPath
from zxptools.xi.mxi.file import AbstractMXIDataFlow, MXIFileData


class Preprocessor(Protocol):
    def setup() -> None: ...
    def get_data_flow(self) -> AbstractMXIDataFlow: ...
    def call() -> None: ...


def concat_js_files(
    files: Iterable[StrOrBytesPath],
    *,
    strict: bool = True,
) -> str:
    file_content = ""

    for file_path in files:
        if not os.path.exists(file_path):
            if strict:
                raise FileNotFoundError(file_path)

            warnings.warn(
                f'JavaScript source file "{file_path}" not found. Skipping...'
            )
            continue

        with open(file_path, "r", encoding="UTF-8", newline="\n") as f:
            file_content += f"{f.read().strip()}\n\n"

    return file_content.rstrip("\n")


class ConcatJSFiles(Preprocessor):
    def __init__(
        self,
        *,
        files: Sequence[pathlib.PurePath],
        arcname: str,
        destination: pathlib.PurePath,
    ) -> None:
        self.arcname: str = arcname
        self.destination: pathlib.PurePath = destination
        self.files: Sequence[pathlib.PurePath] = files

    def get_file_content(self) -> bytes:
        return concat_js_files(
            files=self.files,
            strict=False,
        ).encode()

    def get_data_flow(self) -> MXIFileData:
        return MXIFileData(
            data=self.get_file_content(),
            arcname=pathlib.PurePath(self.arcname),
            destination_dir=self.destination,
            dependencies=list(self.files),
        )


class PreprocessManager:
    def __init__(self, *preprocessors: Preprocessor) -> None:
        self.preprocessors: tuple[Preprocessor, ...] = preprocessors

    def get_data_flow(self) -> Generator[AbstractMXIDataFlow]:
        for preprocessor in self.preprocessors:
            yield preprocessor.get_data_flow()
