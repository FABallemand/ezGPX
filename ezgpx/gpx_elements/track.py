from typing import List

from .extensions import Extensions
from .gpx_element import GpxElement
from .link import Link
from .track_segment import TrackSegment

class Track(GpxElement):
    """
    trkType element in GPX file.
    """
    fields = ["name", "cmt", "desc", "link", "number", "type",
              "extensions", "trkseg"]
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
            type: str = None,
            extensions: Extensions = None,
            trkseg: List[TrackSegment] = None):
        """
        Initialize Track instance.

        Parameters
        ----------
        tag : str, optional
            XML tag, by default "trk"
        name : str, optional
            Name, by default None
        cmt : str, optional
            Comment, by default None
        desc : str, optional
            Description, by default None
        src : str, optional
            Source, by default None
        link : Link, optional
            Link, by default None
        number : int, optional
            Number, by default None
        type : str, optional
            Type, by default None
        extensions : Extensions, optional
            Extensions, by default None
        trkseg : List[TrackSegment], optional
            List of track segments, by default None
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
        self.trkseg: List[TrackSegment] = [] if trkseg is None else trkseg