__all__ = ("ExManVersion",)

import enum

from zxptools.xi import XIVersion


class ExManVersion(enum.Enum):
    MX = XIVersion(1, 6)
    EIGHT = XIVersion(1, 7)
    CS3 = XIVersion(1, 8)
    CS4 = XIVersion(2, 1)
    CS5 = XIVersion(3)  # Placeholder version because idk
    CS6_OR_LATER = XIVersion(4)  # Placeholder version because idk
