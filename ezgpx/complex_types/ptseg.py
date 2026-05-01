"""
This module contains the Ptseg class.
"""

from dataclasses import dataclass
from typing import ClassVar

from .pt import Pt


@dataclass
class Ptseg:
    """
    ptsegType: An ordered sequence of points (e.g.: for polygons or
    polylines).

    Args:
        pt (list[Pt], optional): Ordered list of geographic points.
            Defaults to None.
        tag (str, optional): XML tag. Defaults to "ptseg".
    """

    pt: list[Pt] = None
    tag: str = "ptseg"

    _fields: ClassVar[list[str]] = ["pt"]
    _mandatory_fields: ClassVar[list[str]] = []

    def __post_init__(self):
        if self.pt is not None and (
            not isinstance(self.pt, list) or not all(isinstance(p, Pt) for p in self.pt)
        ):
            raise TypeError("`pt` must be of type list[Pt]")
        if not isinstance(self.tag, str):
            self.tag = str(self.tag)
