"""
This module contains the Trkseg class.
"""

from dataclasses import dataclass
from typing import ClassVar

from .extensions import Extensions
from .wpt import Wpt


@dataclass
class Trkseg:
    """
    trksegType: A Track Segment holds a list of Track Points which are
    logically connected in order. To represent a single GPS track where
    GPS reception was lost, or the GPS receiver was turned off, start a
    new Track Segment for each continuous span of track data.

    Args:
        trkpt (list[Wpt], optional): A Track Point holds the
            coordinates, elevation, timestamp, and metadata for a
            single point in a track. Defaults to None.
        extensions (Extensions, optional): You can add extend GPX by
            adding your own elements from another schema here.
            Defaults to None.
        tag (str, optional): XML tag. Defaults to "trkseg".
    """

    trkpt: list[Wpt] = None
    extensions: Extensions = None
    tag: str = "trkseg"

    _fields: ClassVar[list[str]] = ["trkpt", "extensions"]
    _mandatory_fields: ClassVar[list[str]] = []

    def __post_init__(self):
        if self.trkpt is not None and (
            not isinstance(self.trkpt, list)
            or not all(isinstance(p, Wpt) for p in self.trkpt)
        ):
            raise TypeError("`trkpt` must be of type list[Wpt]")
        if self.extensions is not None and not isinstance(self.extensions, Extensions):
            raise TypeError("`extensions` must be of type Extensions")
        if not isinstance(self.tag, str):
            self.tag = str(self.tag)
