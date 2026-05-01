"""
This module contains the Bounds class.
"""

from dataclasses import dataclass
from typing import ClassVar

from ..simple_types import Latitude, Longitude


@dataclass
class Bounds:
    """
    boundsType: Two lat/lon pairs defining the extent of an element.

    Args:
        minlat (Latitude): Minimum latitude. (in degrees).
        minlon (Longitude): Minimum longitude (in degrees).
        maxlat (Latitude): Maximum latitude (in degrees).
        maxlon (Longitude): Maximum longitude (in degrees).
        tag (str, optional): XML tag. Defaults to "bounds".
    """

    minlat: Latitude
    minlon: Longitude
    maxlat: Latitude
    maxlon: Longitude
    tag: str = "bounds"

    _fields: ClassVar[list[str]] = ["minlat", "minlon", "maxlat", "maxlon"]
    _mandatory_fields: ClassVar[list[str]] = ["minlat", "minlon", "maxlat", "maxlon"]

    def __post_init__(self):
        if not isinstance(self.minlat, Latitude):
            self.minlat = Latitude(self.minlat)
        if not isinstance(self.minlon, Longitude):
            self.minlon = Longitude(self.minlon)
        if not isinstance(self.maxlat, Latitude):
            self.maxlat = Latitude(self.maxlat)
        if not isinstance(self.maxlon, Longitude):
            self.maxlon = Longitude(self.maxlon)
        if not isinstance(self.tag, str):
            self.tag = str(self.tag)
