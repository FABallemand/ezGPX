"""
This module contains the PointSegment class.
"""

from .gpx_element import GpxElement
from .point import Point


class PointSegment(GpxElement):
    """
    ptsegType element in GPX file.
    """

    fields = ["pt"]
    mandatory_fields = []

    def __init__(self, tag: str = "ptseg", pt: list[Point] = None) -> None:
        """
        Initialise PointSegment instance.

        Args:
            tag (str, optional): XML tag. Defaults to "ptseg".
            pt (list[Point], optional): List of points. Defaults to None.
        """
        self.tag: str = tag
        self.pt: list[Point] = [] if pt is None else pt
