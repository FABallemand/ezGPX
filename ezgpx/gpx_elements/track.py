from .track_segment import *

class Track():
    """
    Track (trk) element in GPX file.
    """

    def __init__(self, name: str = "", track_segments: list[TrackSegment] = []):
        self.name = name
        self.track_segments = track_segments