"""
This module contains the Track class.
"""

from .extensions import Extensions
from .gpx_element import GpxElement
from .link import Link
from .track_segment import TrackSegment


class Track(GpxElement):
    """
    trkType element in GPX file.
    """

    fields = ["name", "cmt", "desc", "link", "number", "type", "extensions", "trkseg"]
    mandatory_fields = []

    def __init__(
        self,
        tag: str = "trk",
        name: str = None,
        cmt: str = None,
        desc: str = None,
        src: str = None,
        link: Link = None,
        number: int = None,
        type: str = None,  # pylint: disable=redefined-builtin
        extensions: Extensions = None,
        trkseg: list[TrackSegment] = None,
    ) -> None:
        """
        Initialise Track instance.

        Args:
            tag (str, optional): XML tag. Defaults to "trk".
            name (str, optional): Name. Defaults to None.
            cmt (str, optional): Comment. Defaults to None.
            desc (str, optional): Description. Defaults to None.
            src (str, optional): Source. Defaults to None.
            link (Link, optional): Link. Defaults to None.
            number (int, optional): Number. Defaults to None.
            type (str, optional): Type. Defaults to None.
            extensions (Extensions, optional): Extensions. Defaults to None.
            trkseg (list[TrackSegment], optional): List of track
                segments. Defaults to None.
        """
        self.tag: str = tag
        self.name: str = name
        self.cmt: str = cmt
        self.desc: str = desc
        self.src: str = src
        self.link: Link = link
        self.number: int = number
        self.type: str = type
        self.extensions: Extensions = extensions
        self.trkseg: list[TrackSegment] = [] if trkseg is None else trkseg
