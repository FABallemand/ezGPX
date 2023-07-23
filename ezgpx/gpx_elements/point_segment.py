from .point import Point

class PointSegment():
    """
    ptsegType element in GPX file.
    """

    def __init__(
            self,
            tag: str = "ptseg",
            points: list[Point] = None) -> None:
        """
        Initialize PointSegment instance.

        Args:
            tag (str, optional): XML tag. Defaults to "ptseg".
            points (list[Point], optional): List of points. Defaults to None.
        """
        self.tag: str = tag
        if points is None:
            self.points: list[Point] = []
        else:
            self.points: list[Point] = points