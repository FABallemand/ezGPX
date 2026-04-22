"""
This module contains the DgpsStation class.
"""

from dataclasses import dataclass


@dataclass
class DgpsStation:
    """
    dgpsStationType.

    Args:
        value (int): differential GPS station. Must be in [0, 1023].
    """

    value: int

    def __post_init__(self):
        try:
            self.value = int(self.value)
        except (TypeError, ValueError) as e:
            raise TypeError("value must be convertible to int") from e

        if not 0 <= self.value <= 1023:
            raise ValueError("value must be in [0, 1023]")
