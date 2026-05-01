"""
This module contains the Trk class.
"""

from dataclasses import dataclass
from typing import ClassVar

from .extensions import Extensions
from .link import Link
from .trkseg import Trkseg


@dataclass
class Trk:  # pylint: disable=too-many-instance-attributes
    """
    trkType: trk represents a track - an ordered list of points
    describing a path.

    Args:
        name (str, optional): GPS name of track. Defaults to None.
        cmt (str, optional): GPS comment for track. Defaults to None.
        desc (str, optional): User description of track.
            Defaults to None.
        src (str, optional): Source of data. Included to give user some
            idea of reliability and accuracy of data. Defaults to None.
        link (list[Link], optional): Links to external information
            about track. Defaults to None.
        number (int, optional): GPS track number. Defaults to None.
        type (str, optional): Type (classification) of track.
            Defaults to None.
        extensions (Extensions, optional): You can add extend GPX by
            adding your own elements from another schema here.
            Defaults to None.
        trkseg (list[Trkseg], optional): A Track Segment holds a list
            of Track Points which are logically connected in order.
            To represent a single GPS track where GPS reception was
            lost, or the GPS receiver was turned off, start a new
            Track Segment for each continuous span of track data.
            Defaults to None.
        tag (str, optional): XML tag. Defaults to "trk".
    """

    name: str = None
    cmt: str = None
    desc: str = None
    src: str = None
    link: list[Link] = None
    number: int = None
    type: str = None
    extensions: Extensions = None
    trkseg: list[Trkseg] = None
    tag: str = "trk"

    _fields: ClassVar[list[str]] = [
        "name",
        "cmt",
        "desc",
        "src",
        "link",
        "number",
        "type",
        "extensions",
        "trkseg",
    ]
    _mandatory_fields: ClassVar[list[str]] = []

    def __post_init__(self):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)
        if self.cmt is not None and not isinstance(self.cmt, str):
            self.cmt = str(self.cmt)
        if self.desc is not None and not isinstance(self.desc, str):
            self.desc = str(self.desc)
        if self.src is not None and not isinstance(self.src, str):
            self.src = str(self.src)
        if self.link is not None and (
            not isinstance(self.link, list)
            or not all(isinstance(ll, Link) for ll in self.link)
        ):
            raise TypeError("`link` must be of type list[Link]")
        if self.number is not None and not isinstance(self.number, int):
            self.number = int(self.number)
        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)
        if self.extensions is not None and not isinstance(self.extensions, Extensions):
            raise TypeError("`extensions` must be of type Extensions")
        if self.trkseg is not None and (
            not isinstance(self.trkseg, list)
            or not all(isinstance(t, Trkseg) for t in self.trkseg)
        ):
            raise TypeError("`trkseg` must be of type list[Wpt]")
        if not isinstance(self.tag, str):
            self.tag = str(self.tag)
