from .track_segment import *

class Track():
    """
    Track (trk) element in GPX file.
    """

    def __init__(self, name: str = "", track_segments: list[TrackSegment] = []):
        self.name: str = name
        self.track_segments: list[TrackSegment] = track_segments