"""
This module contains the Fix class.
"""

from dataclasses import dataclass
from enum import Enum


class FixType(str, Enum):
    """
    Values of fixType.
    """

    NONE = "none"
    D2 = "2d"
    D3 = "3d"
    DGPS = "dgps"
    PPS = "pps"


@dataclass
class Fix:
    """
    fixType.

    Args:
        value (FixType): Type of GPS fix.
            Must be one of "none", "2d", "3d", "dgps", "pps".
            "none" means GPS had no fix.
            "pps" means military signal used
            To signify "the fix info is unknown, leave out fixType
            entirely.

    """

    value: FixType

    def __post_init__(self):
        if isinstance(self.value, str):
            try:
                self.value = FixType(self.value.lower())
            except ValueError as e:
                raise ValueError(
                    '`value` must be one of "none", "2d", "3d", "dgps", "pps".'
                ) from e
        elif not isinstance(self.value, FixType):
            raise TypeError("`value` must be of type string or FixType")
