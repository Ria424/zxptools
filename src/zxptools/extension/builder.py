__all__ = ("Builder",)

import os
import warnings
import zipfile
from typing import Protocol, TypeVar

from zxptools.path_token import replace_path_token
from zxptools.type import StrOrBytesPath
from zxptools.xi.mxi import MXI, MXIBuilder


class BaseMXIBuilder(Protocol):
    def build(self, extension_info: MXI) -> str: ...


T = TypeVar("T", bound=BaseMXIBuilder)


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
        mxi_builder: BaseMXIBuilder = MXIBuilder(),
        extension_info_arcname: str = "extension_info.mxi",
    ) -> None:
        self.extension_info: MXI = extension_info
        self.mxi_builder: BaseMXIBuilder = mxi_builder
        self.extension_info_arcname = extension_info_arcname

    def build(self, destination: StrOrBytesPath) -> None:
        with zipfile.ZipFile(
            os.fsdecode(destination), "w", compression=zipfile.ZIP_DEFLATED
        ) as zxp:
            if self.extension_info.files is not None:
                for file in self.extension_info.files:
                    zxp.write(
                        file.get_source(),
                        file.get_arcname(),
                    )

            zxp.writestr(
                self.extension_info_arcname,
                self.mxi_builder.build(self.extension_info),
            )

    def build_direct(self, *, must_exist: bool = True, **tokens: str) -> None:
        if self.extension_info.files is None:
            return

        for file in self.extension_info.files:
            file_source = file.get_source()
            if not os.path.exists(file_source):
                if must_exist:
                    raise FileNotFoundError(file_source)

                warnings.warn(f'FileNotFound: "{file_source}"')
                continue

            with open(file.get_source(), "r", encoding="utf-8") as source_file:
                dest_path = os.path.normpath(
                    os.sep.join(
                        (
                            replace_path_token(
                                file.get_destination_dirname().as_posix(),
                                **tokens,
                            ),
                            os.path.basename(file.get_arcname()),
                        )
                    )
                )
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                with open(
                    dest_path,
                    "w",
                    encoding="utf-8",
                ) as dest_file:
                    dest_file.write(source_file.read())
