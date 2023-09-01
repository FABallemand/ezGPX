from typing import List

from .point import Point

class PointSegment():
    """
    ptsegType element in GPX file.
    """

    def __init__(
            self,
            tag: str = "ptseg",
            points: List[Point] = None) -> None:
        """
        Initialize PointSegment instance.

        Args:
            tag (str, optional): XML tag. Defaults to "ptseg".
            points (List[Point], optional): List of points. Defaults to None.
        """
        self.tag: str = tag
        if points is None:
            self.points: List[Point] = []
        else:
            self.points: List[Point] = points