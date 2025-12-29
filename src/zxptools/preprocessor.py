import inspect
import os
import warnings
from collections.abc import Iterable, Sequence
from typing import ClassVar

from zxptools.type import XMLElementLike


class Preprocessor:
    name: ClassVar[str]

    def __init_subclass__(cls, **kwargs) -> None:
        spec = inspect.getfullargspec(cls.run)
        if spec.varargs is not None:
            raise Exception(
                f"{cls.__name__}.run: Caused by \"*{spec.varargs}\" parameter. '*' parameter is not supported."
            )
        if spec.varkw is not None:
            raise Exception(
                f"{cls.__name__}.run: Caused by \"**{spec.varkw}\" parameter. '**' parameter is not supported."
            )
        if spec.kwonlyargs:
            raise Exception(
                f'{cls.__name__}.run: Caused by "{'", "'.join(spec.kwonlyargs)}" parameters. keyword-only parameters are not supported.'
            )

    def run(self, xml_element: Sequence[XMLElementLike]) -> str:
        raise NotImplementedError

    def get_watchable_files(self) -> Iterable[str]:
        raise NotImplementedError

    def is_mutatable(self) -> bool:
        raise NotImplementedError


class ConcatJSFiles(Preprocessor):
    __slots__ = (
        "_watchable_files",
        "strict",
    )

    name: ClassVar[str] = "concat_js_files"

    def __init__(self, *, strict: bool = True) -> None:
        self._watchable_files: set[str] = {}
        self.strict = strict

    def run(self, xml_element: Sequence[XMLElementLike]) -> str:
        file_content = ""

        file_sources: tuple[str, ...] = tuple(
            map(lambda e: e.attrib["source"], xml_element[0])
        )

        self._watchable_files.update(file_sources)

        for file_source in file_sources:
            if not os.path.exists(file_source):
                if self.strict:
                    raise FileNotFoundError(file_source)

                warnings.warn(
                    f'JavaScript source file "{file_source}" not found. Skipping...'
                )
                continue

            with open(file_source, "r", encoding="UTF-8", newline="\n") as f:
                file_content += f"{f.read()}\n"

        return file_content.rstrip("\n")

    def get_watchable_files(self) -> Iterable[str]:
        return self._watchable_files.copy()

    def is_mutatable(self) -> bool:
        return True
