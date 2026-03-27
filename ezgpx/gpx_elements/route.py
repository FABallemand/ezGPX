"""
This module contains the Route class.
"""

from .extensions import Extensions
from .gpx_element import GpxElement
from .link import Link
from .waypoint import WayPoint


class Route(GpxElement):
    """
    rteType element in GPX file.
    """

    fields = [
        "name",
        "cmt",
        "desc",
        "src",
        "link",
        "number",
        "type",
        "extensions",
        "rtept",
    ]
    mandatory_fields = []

    def __init__(
        self,
        tag: str = "rte",
        name: str = None,
        cmt: str = None,
        desc: str = None,
        src: str = None,
        link: Link = None,
        number: int = None,  # non negative integer
        type: str = None,  # pylint: disable=redefined-builtin
        extensions: Extensions = None,
        rtept: list[WayPoint] = None,
    ) -> None:
        """
        Initialise Route instance.

        Args:
            tag (str, optional): XML tag. Defaults to "rte".
            name (str, optional): Name. Defaults to None.
            cmt (str, optional): Comment. Defaults to None.
            desc (str, optional): Description. Defaults to None.
            src (str, optional): Source. Defaults to None.
            link (Link, optional): Link. Defaults to None.
            number (int, optional): Number. Defaults to None.
            type (str, optional): Type. Defaults to None.
            extensions (Extensions, optional): Extensions. Defaults to None.
            rtept (list[WayPoint], optional): List of route points.
                Defaults to None.
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
        self.rtept: list[WayPoint] = [] if rtept is None else rtept
