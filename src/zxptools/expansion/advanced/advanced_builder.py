from zxptools.type import XMLMutableMapping
from zxptools.xi import MXIBuilder, MXIFile


class AdvancedMXIBuilder(MXIBuilder):
    def _get_file_element(self, file: MXIFile) -> XMLMutableMapping:
        return {
            "@source": file.source,
            "@archive": file.arcname,
            "@destination": file.destination_dir,
            "@file-type": "ordinary",
        }
