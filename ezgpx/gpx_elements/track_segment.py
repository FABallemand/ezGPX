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

        Parameters
        ----------
        tag : str, optional
            XML tag, by default "trkseg"
        trkpt : List[WayPoint], optional
            List of track points, by default None
        extensions : Extensions, optional
            Extensions, by default None
        """
        self.tag: str = tag
        self.trkpt: List[WayPoint] = [] if trkpt is None else trkpt
        self.extensions: Extensions = extensions