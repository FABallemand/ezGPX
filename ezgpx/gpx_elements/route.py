import logging

from .extensions import Extensions
from .link import Link
from .way_point import WayPoint

class Route():
    """
    rteType element in GPX file.
    """

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
            rtept: list[WayPoint] = None) -> None:
        """
        Initialize Route instance.

        Args:
            tag (str, optional): XML tag. Defaults to "rte".
            name (str, optional): Name. Defaults to None.
            cmt (str, optional): Comment. Defaults to None.
            desc (str, optional): Description. Defaults to None.
            src (str, optional): Source. Defaults to None.
            link (Link, optional): Link. Defaults to None.
            number (int, optional): Number. Defaults to None.
            extensions (Extensions, optional): Extensions. Defaults to None.
            rtept (list[WayPoint], optional): Route points. Defaults to None.
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
        if rtept is None:
            self.rtept: list[WayPoint] = []
        else:
            self.rtept: list[WayPoint] = rtept