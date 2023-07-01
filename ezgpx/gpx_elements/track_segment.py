from .extensions import Extensions
from .track_point import TrackPoint

class TrackSegment():
    """
    Track segment (trkseg) in GPX file.
    """
    
    def __init__(
            self,
            trkpt: list[TrackPoint] = [],
            extensions: Extensions = None) -> None:
        """
        Initialize TrackSegment instance.

        Args:
            trkpt (list[TrackPoint], optional): List of track points. Defaults to [].
            extensions (Extensions, optional): Extensions. Defaults to None.
        """
        self.trkpt: list[TrackPoint] = trkpt
        self.extensions: Extensions = extensions

    def project(self):
        for point in self.trkpt:
            point.project()