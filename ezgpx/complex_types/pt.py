"""
This module contains the Pt class.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from ..simple_types import Latitude, Longitude


@dataclass
class Pt:
    """
    ptType: Geographic point with optional elevation and time.
    Available for use by other schemas.

    Args:
        lat (Latitude): Latitude of the point (in degrees).
        lon (Longitude): Longitude of the point (in degrees).
        ele (float, optional): Elevation of the point (in meters).
            Defaults to None.
        time (datetime, optional): Time that the point was recorded.
            Defaults to None.
        tag (str, optional): XML tag. Defaults to "pt".
    """

    lat: Latitude
    lon: Longitude
    ele: float = None
    time: datetime = None
    tag: str = "pt"

    _fields: ClassVar[list[str]] = ["lat", "lon", "ele", "time"]
    _mandatory_fields: ClassVar[list[str]] = ["lat", "lon"]

    def __post_init__(self):
        if not isinstance(self.lat, Latitude):
            self.lat = Latitude(self.lat)
        if not isinstance(self.lon, Longitude):
            self.lon = Longitude(self.lon)
        if self.ele is not None and not isinstance(self.ele, float):
            self.ele = float(self.ele)
        if self.time is not None and not isinstance(self.time, datetime):
            raise TypeError("`time` must be of type datetime")
        if not isinstance(self.tag, str):
            self.tag = str(self.tag)
