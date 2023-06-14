from .track_extensions import *
from .track_segment import *

class Track():
    """
    Track (trk) element in GPX file.
    """

    def __init__(self, name: str = "", track_extensions: TrackExtensions = None, track_segments: list[TrackSegment] = []):
        self.name: str = name
        self.track_extensions: TrackExtensions = track_extensions
        self.track_segments: list[TrackSegment] = track_segments