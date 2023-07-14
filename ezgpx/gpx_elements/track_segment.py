from .extensions import Extensions
from .way_point import WayPoint

class TrackSegment():
    """
    trksegType in GPX file.
    """
    
    def __init__(
            self,
            tag: str = "trkseg",
            trkpt: list[WayPoint] = [],
            extensions: Extensions = None) -> None:
        """
        Initialize TrackSegment instance.

        Args:
        tag (str, optional): XML tag. Defaults to "trkseg".
            trkpt (list[WayPoint], optional): List of track points. Defaults to [].
            extensions (Extensions, optional): Extensions. Defaults to None.
        """
        self.tag: str = tag
        self.trkpt: list[WayPoint] = trkpt
        self.extensions: Extensions = extensions

    def project(self, projection: str):
        """
        Project points.

        Args:
            projection (str): Projection.
        """
        for point in self.trkpt:
            point.project(projection)