"""
This module contains the Point class.
"""

import datetime

from .gpx_element import GpxElement


class Point(GpxElement):
    """
    ptType element in GPX file.
    """

    fields = ["lat", "lon", "ele", "time"]
    mandatory_fields = ["lat", "lon"]

    def __init__(
        self,
        tag: str = "pt",
        lat: float = None,
        lon: float = None,
        ele: float = None,
        time: datetime = None,
    ) -> None:
        """
        Initialise Point instance.

        Args:
            tag (str, optional): XML tag. Defaults to "pt".
            lat (float, optional): Latitude (in degrees). Defaults to None.
            lon (float, optional): Longitude (in degrees). Defaults to None.
            ele (float, optional): Elevation (in meters). Defaults to None.
            time (datetime, optional): Time. Defaults to None.
        """
        self.tag: str = tag
        self.lat: float = lat
        self.lon: float = lon
        self.ele: float = ele
        self.time: datetime = time
