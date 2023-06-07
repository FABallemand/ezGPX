from .track_segment import *

class Track():

    def __init__(self, name: str = "", track_segments: list[TrackSegment] = []):
        self.name = name
        self.track_segments = track_segments