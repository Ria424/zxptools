__all__ = ("AdvancedMXIBuilder",)

from zxptools.xi.mxi import AbstractMXIFile, MXIBuilder


class AdvancedMXIBuilder(MXIBuilder):
    def _get_file_element_attributes(
        self, file: AbstractMXIFile
    ) -> dict[str, str]:
        attributes: dict[str, str] = super()._get_file_element_attributes(file)

        if file.arcname != file.source:
            attributes["@archive"] = file.arcname.as_posix()

        return attributes
