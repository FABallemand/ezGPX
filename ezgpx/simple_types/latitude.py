"""
This module contains the Latitude class.
"""

from dataclasses import dataclass


@dataclass
class Latitude:
    """
    latitudeType.

    Args:
        value (float): Latitude of the point. Decimal degrees, WGS84
            datum. Must be in [-90.0, 90.0].
    """

    value: float

    def __post_init__(self):
        try:
            self.value = float(self.value)
        except (TypeError, ValueError) as e:
            raise TypeError("`value` must be convertible to float") from e

        if not -90 <= self.value <= 90:
            raise ValueError("`value` must be in [-90.0, 90.0]")
