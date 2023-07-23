from .extensions import *
from .link import Link
from .track_segment import *

class Track():
    """
    trkType element in GPX file.
    """

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
            trkseg: list[TrackSegment] = None):
        """
        Initialize Track instance.

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
            trkseg (list[TrackSegment], optional): List of track segments. Defaults to None.
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
        if trkseg is None:
            self.trkseg: list[TrackSegment] = trkseg
        else:
            self.trkseg: list[TrackSegment] = trkseg

    def project(self, projection: str):
        """
        Project segments.

        Args:
            projection (str): Projection.
        """
        for segment in self.trkseg:
            segment.project(projection)