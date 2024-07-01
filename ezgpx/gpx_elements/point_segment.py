from typing import List

from .point import Point

class PointSegment():
    """
    ptsegType element in GPX file.
    """
    fields = ["pt"]
    mandatory_fields = []

    def __init__(
            self,
            tag: str = "ptseg",
            pt: List[Point] = None) -> None:
        """
        Initialize PointSegment instance.

        Parameters
        ----------
        tag : str, optional
            XML tag, by default "ptseg"
        pt : List[Point], optional
            List of points, by default None
        """
        self.tag: str = tag
        self.pt: List[Point] = [] if pt is None else pt