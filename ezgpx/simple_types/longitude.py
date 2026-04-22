"""
This module contains the Longitude class.
"""

from dataclasses import dataclass


@dataclass
class Longitude:
    """
    latitudeType.

    Args:
        value (float): Longitude of the point. Decimal degrees, WGS84
            datum. Must be in [-180.0, 180.0).
    """

    value: float

    def __post_init__(self):
        try:
            self.value = float(self.value)
        except (TypeError, ValueError) as e:
            raise TypeError("value must be convertible to float") from e

        if not -180 <= self.value < 180:
            raise ValueError("value must be in [-180.0, 180.0)")
