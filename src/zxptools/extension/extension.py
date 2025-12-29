__all__ = ("Extension",)

import os
import time
import zipfile
from collections.abc import Iterable

from lxml import etree
from watchdog.events import (
    FileSystemEvent,
    FileSystemEventHandler,
)
from watchdog.observers import Observer

from zxptools.type import StrOrBytesPath
from zxptools.zxp.endpoint import (
    AbstractZxpFileEndpoint,
    AbstractZxpSourceFileEndpoint,
    zxp_write,
)
from zxptools.extension.data import MXI, MXIFileElement


class Extension:
    __slots__ = ("extension_data_path",)

    def __init__(
        self,
        *,
        extension_data_path: StrOrBytesPath,
    ) -> None:
        self.extension_data_path = extension_data_path

    def get_endpoints(self) -> Iterable[AbstractZxpFileEndpoint]:
        

    def build(self, extension_output_path: StrOrBytesPath) -> None:
        extension_info = MXI.load(self.extension_data_path)

        os.makedirs(os.path.dirname(extension_output_path), exist_ok=True)

        with zipfile.ZipFile(
            file=os.fsdecode(extension_output_path), mode="w"
        ) as zxp_file:
            for fileinfo in self.include_getter():
                zxp_write(zxp_file, fileinfo)

                extension_info.files.append(
                    MXIFileElement(
                        source=fileinfo.get_arcname().as_posix(),
                        destination=fileinfo.get_destination_dirname().as_posix(),
                    )
                )

            zxp_file.writestr(
                zinfo_or_arcname="extension_data.mxi",
                data=etree.tostring(
                    extension_info.dump(),
                    encoding="UTF-8",
                    xml_declaration=True,
                ),
            )

    def watch(self) -> None:
        FLASH_CONFIG_DIR: str = os.path.normcase(
            os.path.abspath(os.path.expandvars(os.environ["FLASH_CONFIG_DIR"]))
        )

        watch_files: dict[bytes, str] = {}

        def update_watch_files() -> None:
            nonlocal watch_files

            watch_files = {
                os.path.normcase(
                    os.path.abspath(os.fsencode(file.get_source().as_posix()))
                ): os.path.normcase(
                    os.path.join(
                        file.get_destination_dirname()
                        .as_posix()
                        .replace("$flash", FLASH_CONFIG_DIR),
                        file.get_arcname(),
                    )
                )
                for file in filter(
                    lambda i: isinstance(i, AbstractZxpSourceFileEndpoint),
                    self.include_getter(),
                )
            }

        update_watch_files()

        class MyEventHandler(FileSystemEventHandler):
            def on_any_event(self, event: FileSystemEvent) -> None:
                modified_file = os.path.normcase(
                    os.path.abspath(os.fsencode(event.src_path))
                )

                to_be_modified = watch_files.get(modified_file)
                if to_be_modified is None:
                    return

                print(
                    "2BM:",
                    to_be_modified,
                    "\nORIGINAL:",
                    modified_file,
                )

                with open(to_be_modified, "wb") as destf:
                    with open(event.src_path, "rb") as srcf:
                        destf.write(srcf.read())

                update_watch_files()

        observer = Observer()
        observer.schedule(MyEventHandler(), ".", recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Ctrl+C detected. Shutting down...")
        finally:
            observer.stop()
            observer.join()
