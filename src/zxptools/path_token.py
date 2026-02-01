__all__ = (
    "DEFAULT_TOKENS",
    "replace_path_token",
)

import os
import struct
import warnings
from typing import NamedTuple


def is_32bit() -> bool:
    return struct.calcsize("P") * 8 == 32


class DefaultPathToken(NamedTuple):
    macos: str | None
    windows: str | None
    help: str | None = None


DEFAULT_TOKENS = {
    "system": DefaultPathToken(
        "/System",
        "C:\\Windows\\system32" if is_32bit() else "C:\\Windows\\SysWOW64",
    ),
    "system64": DefaultPathToken("/System", "C:\\Windows\\system32"),
    "fonts": DefaultPathToken("/Library/Fonts", "C:\\Windows\\Fonts"),
    "flash": DefaultPathToken(
        None,
        None,
        help=(
            (
                '''$flash token value may be in "C:\\Users\\<User name>\\AppData\\Local\\Adobe\\<Flash or Animate product name>\\<Locale>\\Configuration".
For Example: "C:\\Users\\CoolUser\\AppData\\Local\\Adobe\\Animate 2024\\en_US\\Configuration"'''
            )
            if os.name == "nt"
            else (
                '''$flash token value may be in "/Users/<User name>/Library/Application Support/Adobe/<Flash or Animate product name>/<Locale>/Configuration".
For Example: "/Users/CoolUser/Library/Application Support/Adobe/Animate 2024/en_US/Configuration"'''
            )
        ),
    ),
}


def replace_path_token(s: str, **custom_tokens) -> str:
    print(f'"{s}" -> ', end="")

    path_tokens = {
        name: token_value.windows if os.name == "nt" else token_value.macos
        for name, token_value in DEFAULT_TOKENS.items()
    }
    path_tokens.update(custom_tokens)

    for name, path in path_tokens.items():
        if s.startswith(f"${name}"):
            if path is None:
                error_msg = f'Cannot find default token value for "${name}". Please provide token value by yourself.'
                if (help_msg := DEFAULT_TOKENS[name].help) is not None:
                    error_msg += f'\nHere is some helpful message from "${name}" token:\n\n{help_msg}'
                raise ValueError(error_msg)

            if not os.path.isabs(path):
                raise ValueError(
                    f'"${name}" token value must be an absolute path.'
                )

            if os.path.exists(path):
                s = os.path.normpath(
                    os.sep.join(
                        (
                            path,
                            s.removeprefix(f"${name}"),
                        )
                    )
                )
                print(f'"{s}"')
            else:
                warnings.warn(
                    f'Couldn\'t reslove token "${name}" because "{path}" doesn\'t exist.'
                )

            break
    return s
