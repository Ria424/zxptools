import pathlib

from zxptools import util
from zxptools.xi import MXIFile, MXIParser


class AdvancedMXIParser(MXIParser):
    def _parse_file_element(self, file_element) -> MXIFile:
        archive_path = util.xml.get_attrib(file_element, "archive")
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
