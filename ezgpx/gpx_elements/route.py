from typing import List
from .extensions import Extensions
from .gpx_element import GpxElement
from .link import Link
from .way_point import WayPoint

class Route(GpxElement):
    """
    rteType element in GPX file.
    """
    fields = ["name", "cmt", "desc", "src", "link", "number", "type",
              "extensions", "rtept"]
    mandatory_fields = []

    def __init__(
            self,
            tag: str = "rte",
            name: str = None,
            cmt: str = None,
            desc: str = None,
            src: str = None,
            link: Link = None,
            number: int = None, # non negative integer
            type: str = None,
            extensions: Extensions = None,
            rtept: List[WayPoint] = None) -> None:
        """
        Initialize Route instance.

        Parameters
        ----------
        tag : str, optional
            XML tag, by default "rte"
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
        extensions : Extensions, optional
            Extensions, by default None
        rtept : List[WayPoint], optional
            Route points, by default None
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
        self.rtept: List[WayPoint] = [] if rtept is None else rtept