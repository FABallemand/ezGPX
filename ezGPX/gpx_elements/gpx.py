from .metadata import *
from .track import *

class GPX():

    def __init__(self, metadata: Metadata = None, tracks: list[Track] = []):
        self.metadata = metadata
        self.tracks = tracks