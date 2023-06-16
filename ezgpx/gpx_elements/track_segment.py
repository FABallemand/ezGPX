from .extensions import Extensions
from .track_point import TrackPoint

class TrackSegment():
    """
    Track segment (trkseg) in GPX file.
    """
    
    def __init__(
            self,
            trkpt: list[TrackPoint] = [],
            extensions: Extensions = None):
        self.trkpt: list[TrackPoint] = trkpt
        self.extensions: Extensions = extensions