__all__ = ("AdvancedMXIParser",)

import pathlib
from typing import Any

from zxptools import util
from zxptools.xi.mxi import MXIFile, MXIParser


class AdvancedMXIParser(MXIParser):
    def _parse_file_element(self, file_element: Any) -> MXIFile:
        super()._parse_file_element(file_element)
        archive_path: str | None = util.xml.get_attrib(file_element, "archive")

        return MXIFile(
            source=pathlib.PurePath(
                util.xml.get_attrib(file_element, "source", strict=True)
            ),
            destination_dir=pathlib.PurePath(
                util.xml.get_attrib(file_element, "destination", strict=True)
            ),
            arcname=(
                pathlib.PurePath(archive_path)
                if archive_path is not None
                else None
            ),
        )
