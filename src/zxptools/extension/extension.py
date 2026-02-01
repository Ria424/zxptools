import re

__all__ = ("Extension",)

import argparse
import os

from zxptools.extension.builder import Builder
from zxptools.extension.watcher import Watcher
from zxptools.type import StrOrBytesPath
from zxptools.xi import MXI


class Extension:
    __slots__ = (
        "builder",
        "extension_info",
        "watcher",
    )

    def __init__(
        self,
        extension_info: MXI,
        builder: Builder | None = None,
    ) -> None:
        self.extension_info: MXI = extension_info
        self.builder: Builder = (
            builder if builder is not None else Builder(self.extension_info)
        )
        self.watcher: Watcher = Watcher(self.builder)

    def build(self, destination: StrOrBytesPath) -> None:
        self.builder.build(destination)

    def watch(self, **tokens: str) -> None:
        if not self.extension_info.files:
            return

        for file in self.extension_info.files:
            self.watcher.add_dependency(file)

        self.watcher.watch(**tokens)

    def get_argument_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser("Extension Builder/Watcher")
        sub_parsers = parser.add_subparsers()
        build_parser = sub_parsers.add_parser("build")
        build_parser.set_defaults(mode="build")
        build_parser.add_argument("destination")
        watch_parser = sub_parsers.add_parser("watch")
        watch_parser.set_defaults(mode="watch")
        watch_parser.add_argument("-t", "path_token", action="store_const")
        return parser

    def run_argument_parser(self) -> None:
        parser = self.get_argument_parser()
        args = parser.parse_args()

        if args.mode == "build":
            os.makedirs(os.path.dirname(args.destination))
            self.build(args.destination)

        if args.mode == "watch":
            path_tokens_regex = re.compile(r"^([a-zA-Z]+)=(/.*)$")
            self.watch()
