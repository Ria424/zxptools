__all__ = ("Extension",)

import argparse
import os
import re
from typing import Literal

from zxptools.extension.building import Builder
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
        *,
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
        if not self.extension_info.data_flow:
            return

        for data_flow in self.extension_info.data_flow:
            self.watcher.update_dependency(*data_flow.dependencies)

        self.watcher.watch(**tokens)

    def get_argument_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser("Extension Builder/Watcher")
        sub_parsers = parser.add_subparsers()

        build_parser = sub_parsers.add_parser("build")
        build_parser.set_defaults(mode="build")
        build_parser.add_argument(
            "-o", dest="output", action="store", required=True
        )

        watch_parser = sub_parsers.add_parser("watch")
        watch_parser.set_defaults(mode="watch")
        watch_parser.add_argument(
            "-t", dest="path_tokens", action="append", default=[]
        )

        return parser

    def run_argument_parser(self) -> None:
        parser = self.get_argument_parser()
        args = parser.parse_args()

        if "mode" not in args:
            parser.error("MISSING [build | watch]")

        mode: Literal["build", "watch"] = args.mode

        if mode == "build":
            output: str = args.output

            if output_dirname := os.path.dirname(output):
                os.makedirs(output_dirname, exist_ok=True)

            self.build(output)
        elif mode == "watch":
            path_tokens: list[str] = args.path_tokens

            if path_tokens:
                if os.name == "nt":
                    path_tokens_regex: re.Pattern[str] = re.compile(
                        r'^([a-zA-Z]+)=([a-zA-Z]:[\\/][^<>:"|?*]*)$'
                    )
                else:
                    path_tokens_regex: re.Pattern[str] = re.compile(
                        r"^([a-zA-Z]+)=(/.*)$"
                    )

                for path_token_pair in path_tokens:
                    match: re.Match[str] | None = path_tokens_regex.match(
                        path_token_pair
                    )
                    if match is None:
                        raise ValueError(
                            f'Invaild path token: "{path_token_pair}"'
                        )

                    path_token_name: str = match.group(1)
                    path_token_value: str = match.group(2)
                    print(f'${path_token_name}="{path_token_value}"')
                    self.watcher.tokens[path_token_name] = path_token_value

            self.watch()
