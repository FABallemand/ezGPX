"""
This module contains the Bounds class.
"""

from .gpx_element import GpxElement


class Bounds(GpxElement):
    """
    boundsType element in GPX file.
    """

    fields = ["minlat", "minlon", "maxlat", "maxlon"]
    mandatory_fields = ["minlat", "minlon", "maxlat", "maxlon"]

    def __init__(
        self,
        tag: str = "bounds",
        minlat: float = None,
        minlon: float = None,
        maxlat: float = None,
        maxlon: float = None,
    ) -> None:
        """
        Initialise Bounds instance.

        Args:
            tag (str, optional): XML tag. Defaults to "bounds".
            minlat (float, optional): Minimal latitude (in degrees).
                Defaults to None.
            minlon (float, optional): Minimal longitude (in degrees).
                Defaults to None.
            maxlat (float, optional): Maximal latitude (in degrees).
                Defaults to None.
            maxlon (float, optional): Maximal longitude (in degrees).
                Defaults to None.
        """
        self.tag: str = tag
        self.minlat: float = minlat
        self.minlon: float = minlon
        self.maxlat: float = maxlat
        self.maxlon: float = maxlon
