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
        if isinstance(self.value, str):
            try:
                self.value = int(self.value)
            except ValueError as e:
                raise TypeError("`value` must be convertible to int") from e
        elif not isinstance(self.value, int):
            raise TypeError("`value` must be int")

        if not 0 <= self.value <= 1023:
            raise ValueError("`value` must be in [0, 1023]")
