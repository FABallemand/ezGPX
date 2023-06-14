import pandas as pd

from .metadata import *
from .track import *

from ..utils import haversine_distance

class Gpx():
    """
    Gpx (gpx) element in GPX file.
    """

    def __init__(self, metadata: Metadata = None, tracks: list[Track] = []):
        self.metadata: Metadata = metadata
        self.tracks: list[Track]  = tracks

    def distance(self):
        """
        Compute the total distance (in meters) of the tracks contained in the Gpx element.

        Returns:
            float: Distance (meters)
        """
        dst = 0
        previous_latitude = self.tracks[0].track_segments[0].track_points[0].latitude
        previous_longitude = self.tracks[0].track_segments[0].track_points[0].longitude
        for track in self.tracks:
            for track_segment in track.track_segments:
                for track_point in track_segment.track_points:
                    dst += haversine_distance(previous_latitude, previous_longitude, track_point.latitude, track_point.longitude)
                    previous_latitude = track_point.latitude
                    previous_longitude = track_point.longitude
        return dst

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
    
    def remove_gps_errors(self, error_distance=1000):
        """
        Remove GPS errors.

        Args:
            error_distance (int, optional): GPS error threshold distance (meters) between two points. Defaults to 1000.

        Returns:
            list: List of removed points (GPS errors).
        """
        previous_point = None
        gps_errors = []

        for track in self.tracks:
            for track_segment in track.track_segments:
                for track_point in track_segment.track_points:
                    # Create points
                    if previous_point is not None and haversine_distance(previous_point.latitude,
                                                                         previous_point.longitude,
                                                                         track_point.latitude,
                                                                         track_point.longitude) < error_distance:
                        gps_errors.append(track_point)
                        track_segment.track_points.remove(track_point)
                    else:
                        previous_point = track_point    
        return gps_errors

    def remove_points(self, remove_factor: int = 2):
        count = 0
        for track in self.tracks:
            for track_segment in track.track_segments:
                for track_point in track_segment.track_points:
                    if count % remove_factor == 0:
                        track_segment.track_points.remove(track_point)
                        count += 1