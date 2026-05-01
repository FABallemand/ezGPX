"""
This module contains the Rte class.
"""

from dataclasses import dataclass
from typing import ClassVar

from .extensions import Extensions
from .link import Link
from .wpt import Wpt


@dataclass
class Rte:  # pylint: disable=too-many-instance-attributes
    """
    rteType: Route - an ordered list of waypoints representing a series
    of turn points leading to a destination.

    Args:
        name (str, optional): GPS name of route. Defaults to None.
        cmt (str, optional): GPS comment for route. Defaults to None.
        desc (str, optional): Text description of route for user. Not
            sent to GPS. Defaults to None.
        src (str, optional): Source of data. Included to give user some
            idea of reliability and accuracy of data. Defaults to None.
        link (list[Link], optional): Links to external information
            about the route. Defaults to None.
        number (int, optional): GPS route number. Defaults to None.
        type (str, optional): Type (classification) of route.
            Defaults to None.
        extensions (Extensions, optional): You can add extend GPX by
            adding your own elements from another schema here.
            Defaults to None.
        rtept (list[Wpt], optional): List of route points.
            Defaults to None.
        tag (str, optional): XML tag. Defaults to "rte".
    """

    name: str = None
    cmt: str = None
    desc: str = None
    src: str = None
    link: list[Link] = None
    number: int = None
    type: str = None
    extensions: Extensions = None
    rtept: list[Wpt] = None
    tag: str = "rte"

    _fields: ClassVar[list[str]] = [
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
        if self.rtept is not None and (
            not isinstance(self.rtept, list)
            or not all(isinstance(p, Wpt) for p in self.rtept)
        ):
            raise TypeError("`rtept` must be of type list[Wpt]")
        if not isinstance(self.tag, str):
            self.tag = str(self.tag)
