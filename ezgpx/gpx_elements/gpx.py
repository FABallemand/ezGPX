import pandas as pd

from .metadata import *
from .track import *

class Gpx():
    """
    Gpx (gpx) element in GPX file.
    """

    def __init__(self, metadata: Metadata = None, tracks: list[Track] = []):
        self.metadata: Metadata = metadata
        self.tracks: list[Track]  = tracks

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert Gpx element to Pandas Dataframe.

        Returns:
            pd.DataFrame: Dataframe containing position data from GPX.
        """
        route_info = []
        for track in self.tracks:
            for segment in track.track_segments:
                for point in segment.track_points:
                    route_info.append({
                        "latitude": point.latitude,
                        "longitude": point.longitude,
                        "elevation": point.elevation
                    })
        df = pd.DataFrame(route_info)
        return df

    def remove_points(self, remove_factor: int = 2):
        count = 0
        for track in self.tracks:
            for track_segment in track.track_segments:
                for track_point in track_segment.track_points:
                    if count % remove_factor == 0:
                        track_segment.track_points.remove(track_point)
                        count += 1