"""
This module contains the Degrees class.
"""

from dataclasses import dataclass


@dataclass(order=True)
class Degrees:
    """
    degreesType.

    Args:
        value (float): Degrees value used for bearing, heading, course.
            Units are decimal degrees, true (not magnetic).
            Must be in [0.0, 360.0).
    """

    value: float

    def __post_init__(self):
        try:
            self.value = float(self.value)
        except (TypeError, ValueError) as e:
            raise TypeError("`value` must be convertible to float") from e

        if not 0 <= self.value < 360:
            raise ValueError("`value` must be in [0.0, 360.0)")
