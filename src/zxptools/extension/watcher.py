__all__ = ("Watcher",)

import logging
import os
import time
from collections.abc import Callable
from typing import Any

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

from zxptools.extension.builder import Builder


class WatchEventHandler(PatternMatchingEventHandler):
    __slots__ = (
        "build_func",
        "logger",
    )

    def __init__(self, *, parent: Any, patterns: list[str]) -> None:
        super().__init__(patterns=patterns)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger("test")
        self.logger.setLevel(logging.INFO)

        self.parent = parent

    def callback(self) -> None:
        self.parent.callback()

    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
        super().on_moved(event)

        what = "directory" if event.is_directory else "file"
        self.logger.info(
            "Moved %s: from %s to %s", what, event.src_path, event.dest_path
        )

        self.callback()

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        super().on_created(event)

        what = "directory" if event.is_directory else "file"
        self.logger.info("Created %s: %s", what, event.src_path)

        self.callback()

    def on_deleted(self, event: DirDeletedEvent | FileDeletedEvent) -> None:
        super().on_deleted(event)

        what = "directory" if event.is_directory else "file"
        self.logger.info("Deleted %s: %s", what, event.src_path)

        self.callback()

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        super().on_modified(event)

        what = "directory" if event.is_directory else "file"
        self.logger.info("Modified %s: %s", what, event.src_path)

        self.callback()


class Watcher:
    __slots__ = (
        "_dependencies",
        "builder",
        "callbacks",
        "tokens",
    )

    def __init__(self, builder: Builder) -> None:
        self._dependencies: set[str] = set()
        self.builder: Builder = builder
        self.callbacks: dict[str, Callable[[], None]] = {}
        self.tokens: dict[str, str] = {}

    def add_dependency(self, dependency: str) -> None:
        self._dependencies.add(os.path.normpath(os.path.abspath(dependency)))

    def remove_dependency(self, dependency: str) -> None:
        self._dependencies.remove(
            os.path.normpath(os.path.abspath(dependency))
        )

    def get_dependency(self) -> set[str]:
        return self._dependencies.copy()

    def callback(self) -> None:
        for callback in self.callbacks.values():
            callback()
        self.builder.build_direct(must_exist=False, **self.tokens)

    def watch(self) -> None:
        observer = PollingObserver()
        observer.schedule(
            WatchEventHandler(
                parent=self,
                patterns=list(self._dependencies),
            ),
            os.getcwd(),
            recursive=True,
        )
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
