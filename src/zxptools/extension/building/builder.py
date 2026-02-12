__all__ = ("Builder",)

import os
import warnings
import zipfile
from collections.abc import Callable
from typing import Literal, Protocol

import attrs

from zxptools import path_token
from zxptools.type import SizedBuffer, StrOrBytesPath
from zxptools.xi.mxi import MXI, MXIBuilder, MXIFile, MXIFileData


class MXIBuilderLike(Protocol):
    def build(self, extension_info: MXI) -> str: ...


MXIBuilderCallable = Callable[[MXI], SizedBuffer | str]


@attrs.define
class Builder:
    __slots__ = (
        "extension_info",
        "extension_info_arcname",
        "mxi_builder",
    )

    def __init__(
        self,
        extension_info: MXI,
        *,
        extension_info_arcname: str = "extension_info.mxi",
        mxi_builder: MXIBuilderLike | None = None,
    ) -> None:
        self.extension_info: MXI = extension_info
        self.mxi_builder: MXIBuilderLike = (
            mxi_builder if mxi_builder is not None else MXIBuilder()
        )
        self.extension_info_arcname: str = extension_info_arcname

        if os.path.isabs(self.extension_info_arcname):
            raise ValueError(
                f'extension_info_arcname "{self.extension_info_arcname}" must be a reletive path.'
            )

    def build(
        self,
        destination: StrOrBytesPath,
        *,
        compresslevel: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] | None = None,
    ) -> None:
        with zipfile.ZipFile(
            os.fsdecode(destination),
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=compresslevel,
        ) as zxp:
            for data_flow in self.extension_info.data_flow:
                if isinstance(data_flow, MXIFile):
                    zxp.write(
                        data_flow.source,
                        data_flow.arcname,
                    )
                elif isinstance(data_flow, MXIFileData):
                    zxp.writestr(data_flow.arcname.as_posix(), data_flow.data)

            zxp.writestr(
                self.extension_info_arcname,
                self.mxi_builder.build(self.extension_info),
            )

    def build_direct(self, *, must_exist: bool = True, **tokens: str) -> None:
        if not self.extension_info.data_flow:
            return

        for data_flow in self.extension_info.data_flow:
            dest_path = os.path.normpath(
                os.sep.join(
                    (
                        path_token.replace_path_token(
                            data_flow.destination_dir.as_posix(),
                            **tokens,
                        ),
                        os.path.basename(data_flow.arcname),
                    )
                )
            )

            if isinstance(data_flow, MXIFile):
                file_source = data_flow.source
                if not os.path.exists(file_source):
                    if must_exist:
                        raise FileNotFoundError(file_source)

                    warnings.warn(f'FileNotFound: "{file_source}"')
                    continue

                with open(
                    data_flow.source, "r", encoding="UTF-8"
                ) as source_file:
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                    with open(
                        dest_path,
                        "w",
                        encoding="UTF-8",
                    ) as dest_file:
                        dest_file.write(source_file.read())
            elif isinstance(data_flow, MXIFileData):
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                with open(dest_path, "wb") as dest_file:
                    dest_file.write(data_flow.data)
