from .track_point import *

class TrackSegment():

    def __init__(self, track_points: list[TrackPoint] = []):
        self.track_points = track_points