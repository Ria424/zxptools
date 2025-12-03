import os
import zipfile
from collections.abc import Iterable

from lxml import etree

from zxptools.type import StrOrBytesPath
from zxptools.zxp.endpoint import (
    AbstractZxpFileEndpoint,
    zxp_write,
)
from zxptools.zxp.mxi import ExtensionInfo, FileElement


def build_zxp(
    *,
    zxp_file: zipfile.ZipFile,
    extension_info: ExtensionInfo,
    files_to_include: Iterable[AbstractZxpFileEndpoint],
) -> None:
    for file in files_to_include:
        zxp_write(zxp_file, file)

        extension_info.files.append(
            FileElement(
                source=file.get_arcname().as_posix(),
                destination=file.get_destination_dirname().as_posix(),
            )
        )

    zxp_file.writestr(
        zinfo_or_arcname="extension_data.mxi",
        data=etree.tostring(
            extension_info.dump(), encoding="UTF-8", xml_declaration=True
        ),
    )


def build(
    *,
    extension_data_path: StrOrBytesPath,
    extension_output_path: StrOrBytesPath,
    include: Iterable[AbstractZxpFileEndpoint],
) -> None:
    extension_info = ExtensionInfo.load(extension_data_path)

    os.makedirs(os.path.dirname(extension_output_path), exist_ok=True)

    with zipfile.ZipFile(
        file=os.fsdecode(extension_output_path), mode="w"
    ) as zxp_file:
        build_zxp(
            zxp_file=zxp_file,
            extension_info=extension_info,
            files_to_include=include,
        )
