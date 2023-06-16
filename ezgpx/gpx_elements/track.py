from .extensions import *
from .link import Link
from .track_segment import *

class Track():
    """
    Track (trk) element in GPX file.
    """

    def __init__(
            self,
            name: str = None,
            cmt: str = None,
            desc: str = None,
            src: str = None,
            link: Link = None,
            number: int = None,
            type: str = None,
            extensions: Extensions = None,
            trkseg: list[TrackSegment] = []):
        self.name: str = name,
        self.cmt: str = cmt,
        self.desc: str = desc,
        self.src: str = src,
        self.link: Link = link,
        self.number: int = number,
        self.type: str = type,
        self.extensions: Extensions = extensions,
        self.trkseg: list[TrackSegment] = trkseg