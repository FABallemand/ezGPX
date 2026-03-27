"""
This module contains the TrackSegment class.
"""

from .extensions import Extensions
from .gpx_element import GpxElement
from .waypoint import WayPoint


class TrackSegment(GpxElement):
    """
    trksegType element in GPX file.
    """

    fields = ["trkpt", "extensions"]
    mandatory_fields = []

    def __init__(
        self,
        tag: str = "trkseg",
        trkpt: list[WayPoint] = None,
        extensions: Extensions = None,
    ) -> None:
        """
        Initialise TrackSegment instance.

        Args:
            tag (str, optional): XML tag. Defaults to "trkseg".
            trkpt (list[WayPoint], optional): List of track points. Defaults to None.
            extensions (Extensions, optional): Extensions. Defaults to None.
        """
        self.tag: str = tag
        self.trkpt: list[WayPoint] = [] if trkpt is None else trkpt
        self.extensions: Extensions = extensions
