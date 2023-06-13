from .track_point import *

class TrackSegment():
    """
    Track segment (trkseg) in GPX file.
    """
    
    def __init__(self, track_points: list[TrackPoint] = []):
        self.track_points: list[TrackPoint] = track_points