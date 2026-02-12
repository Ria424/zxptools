__all__ = ("Watcher",)

import logging
import os
import pathlib
import time
from collections.abc import Callable

from watchdog.events import (
    DirCreatedEvent,
    DirDeletedEvent,
    DirModifiedEvent,
    DirMovedEvent,
    FileCreatedEvent,
    FileDeletedEvent,
    FileModifiedEvent,
    FileMovedEvent,
    PatternMatchingEventHandler,
)
from watchdog.observers.polling import PollingObserver

from zxptools.extension.building.builder import Builder


class WatcherEventHandler(PatternMatchingEventHandler):
    __slots__ = (
        "callback",
        "logger",
    )

    def __init__(
        self,
        callback: Callable[[], None] | None = None,
        *,
        patterns: list[str],
    ) -> None:
        super().__init__(patterns=patterns)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger: logging.Logger = logging.getLogger("watcher")
        self.logger.setLevel(logging.INFO)

        self.callback = callback

    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
        super().on_moved(event)

        what = "directory" if event.is_directory else "file"
        self.logger.info(
            "Moved %s: from %s to %s", what, event.src_path, event.dest_path
        )

        if self.callback is not None:
            self.callback()

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        super().on_created(event)

        what = "directory" if event.is_directory else "file"
        self.logger.info("Created %s: %s", what, event.src_path)

        if self.callback is not None:
            self.callback()

    def on_deleted(self, event: DirDeletedEvent | FileDeletedEvent) -> None:
        super().on_deleted(event)

        what = "directory" if event.is_directory else "file"
        self.logger.info("Deleted %s: %s", what, event.src_path)

        if self.callback is not None:
            self.callback()

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        super().on_modified(event)

        what = "directory" if event.is_directory else "file"
        self.logger.info("Modified %s: %s", what, event.src_path)

        if self.callback is not None:
            self.callback()


class Watcher:
    __slots__ = (
        "_dependencies",
        "_observer",
        "builder",
        "callback",
        "tokens",
    )

    def __init__(self, builder: Builder) -> None:
        self._dependencies: set[pathlib.PurePath] = set()
        self._observer: PollingObserver = PollingObserver()

        self.builder: Builder = builder
        self.callback: Callable[[], None] | None = None
        self.tokens: dict[str, str] = {}

    def add_dependency(self, dependency: pathlib.PurePath) -> None:
        if self._observer.is_alive():
            raise Exception("Cannot modify dependencies while watching.")
        self._dependencies.add(dependency)

    def update_dependency(self, *dependencies: pathlib.PurePath) -> None:
        if self._observer.is_alive():
            raise Exception("Cannot modify dependencies while watching.")
        self._dependencies.update(dependencies)

    def remove_dependency(self, dependency: pathlib.PurePath) -> None:
        if self._observer.is_alive():
            raise Exception("Cannot modify dependencies while watching.")
        self._dependencies.remove(dependency)

    def get_dependency(self) -> set[pathlib.PurePath]:
        return self._dependencies.copy()

    def sync(self) -> None:
        self.builder.build_direct(must_exist=False, **self.tokens)

    def watch(self) -> None:
        self._observer.schedule(
            WatcherEventHandler(
                self.sync,
                patterns=list(path.as_posix() for path in self._dependencies),
            ),
            os.getcwd(),
            recursive=True,
        )

        self.sync()

        self._observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self._observer.stop()
            self._observer.join()
