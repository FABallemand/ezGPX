from typing import List

from .extensions import Extensions
from .way_point import WayPoint

class TrackSegment():
    """
    trksegType in GPX file.
    """
    
    def __init__(
            self,
            tag: str = "trkseg",
            trkpt: List[WayPoint] = None,
            extensions: Extensions = None) -> None:
        """
        Initialize TrackSegment instance.

        Args:
        tag (str, optional): XML tag. Defaults to "trkseg".
            trkpt (List[WayPoint], optional): List of track points. Defaults to None.
            extensions (Extensions, optional): Extensions. Defaults to None.
        """
        self.tag: str = tag
        if trkpt is None:
            self.trkpt: List[WayPoint] = []
        else:
            self.trkpt: List[WayPoint] = trkpt
        self.extensions: Extensions = extensions

    def project(self, projection: str):
        """
        Project points.

        Args:
            projection (str): Projection.
        """
        for point in self.trkpt:
            point.project(projection)