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

        Parameters
        ----------
        tag : str, optional
            XML tag, by default "ptseg"
        points : List[Point], optional
            List of points, by default None
        """
        self.tag: str = tag
        self.points: List[Point] = [] if points is None else points