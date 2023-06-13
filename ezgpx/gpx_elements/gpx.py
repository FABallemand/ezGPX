import pandas as pd

from .metadata import *
from .track import *

class Gpx():
    """
    Gpx (gpx) element in GPX file.
    """

    def __init__(self, metadata: Metadata = None, tracks: list[Track] = []):
        self.metadata = metadata
        self.tracks = tracks

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
