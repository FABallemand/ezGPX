from datetime import datetime, timezone

import pandas as pd

from .metadata import *
from .track import *

from ..utils import haversine_distance

class Gpx():
    """
    Gpx (gpx) element in GPX file.
    """

    def __init__(
            self,
            creator: str = None,
            xmlns: str = None,
            version: str = None,
            xmlns_xsi: str = None,
            xsi_schema_location: list[str] = None,
            xmlns_gpxtpx: str = None,
            xmlns_gpxx: str = None,
            xmlns_gpxtrk: str = None,
            xmlns_wptx1: str = None,
            metadata: Metadata = None,
            tracks: list[Track] = []):
        self.creator: str = creator
        self.xmlns: str = xmlns
        self.version: str = version

        self.xmlns_xsi: str = xmlns_xsi
        self.xsi_schema_location: str = xsi_schema_location
        self.xmlns_gpxtpx: str = xmlns_gpxtpx
        self.xmlns_gpxx: str = xmlns_gpxx
        self.xmlns_gpxtrk: str = xmlns_gpxtrk
        self.xmlns_wptx1: str = xmlns_wptx1

        self.metadata: Metadata = metadata
        self.tracks: list[Track]  = tracks

    def distance(self) -> float:
        """
        Compute the total distance (meters) of the tracks contained in the Gpx element.

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
    
    def ascent(self) -> float:
        """
        Compute the total ascent (meters) of the tracks contained in the Gpx element.

        Returns:
            float: Ascent (meters)
        """
        ascent = 0
        previous_elevation = self.tracks[0].track_segments[0].track_points[0].elevation
        for track in self.tracks:
            for track_segment in track.track_segments:
                for track_point in track_segment.track_points:
                    if track_point.elevation > previous_elevation:
                        ascent += track_point.elevation - previous_elevation
                    previous_elevation = track_point.elevation
        return ascent
    
    def descent(self) -> float:
        """
        Compute the total descent (meters) of the tracks contained in the Gpx element.

        Returns:
            float: Descent (meters)
        """
        descent = 0
        previous_elevation = self.tracks[0].track_segments[0].track_points[0].elevation
        for track in self.tracks:
            for track_segment in track.track_segments:
                for track_point in track_segment.track_points:
                    if track_point.elevation < previous_elevation:
                        descent += previous_elevation - track_point.elevation
                    previous_elevation = track_point.elevation
        return descent
    
    def min_elevation(self) -> float:
        """
        Compute minimum elevation (meters) in the tracks contained in the Gpx element.

        Returns:
            float: Minimum elevation (meters).
        """
        min_elevation = self.tracks[0].track_segments[0].track_points[0].elevation
        for track in self.tracks:
            for track_segment in track.track_segments:
                for track_point in track_segment.track_points:
                    if track_point.elevation < min_elevation:
                        min_elevation = track_point.elevation
        return min_elevation
    
    def max_elevation(self) -> float:
        """
        Compute maximum elevation (meters) in the tracks contained in the Gpx element.

        Returns:
            float: Maximum elevation (meters).
        """
        max_elevation = self.tracks[0].track_segments[0].track_points[0].elevation
        for track in self.tracks:
            for track_segment in track.track_segments:
                for track_point in track_segment.track_points:
                    if track_point.elevation > max_elevation:
                        max_elevation = track_point.elevation
        return max_elevation
    
    def utc_start_time(self) -> datetime:
        """
        Return the activity UTC starting time.

        Returns:
            datetime: UTC start time.
        """
        return self.tracks[0].track_segments[0].track_points[0].time
    
    def utc_stop_time(self):
        """
        Return the activity UTC stopping time.

        Returns:
            datetime: UTC stop time.
        """
        return self.tracks[-1].track_segments[-1].track_points[-1].time
    
    def start_time(self) -> datetime:
        """
        Return the activity starting time.

        Returns:
            datetime: Start time.
        """
        return self.tracks[0].track_segments[0].track_points[0].time.replace(tzinfo=timezone.utc).astimezone(tz=None) 
    
    def stop_time(self):
        """
        Return the activity stopping time.

        Returns:
            datetime: Stop time.
        """
        return self.tracks[-1].track_segments[-1].track_points[-1].time.replace(tzinfo=timezone.utc).astimezone(tz=None) 
    
    def total_elapsed_time(self) -> datetime:
        """
        Compute the total elapsed time.

        Returns:
            datetime: Total elapsed time.
        """
        return self.stop_time() - self.start_time()
    
    def avg_speed(self) -> float:
        """
        Compute the average speed (kilometers per second) during the activity.

        Returns:
            float: Average speed (kilometers per seconds)
        """
        # Compute and convert total elapsed time
        total_elapsed_time = self.total_elapsed_time()
        total_elapsed_time = total_elapsed_time.total_seconds() / 3600

        # Compute and convert distance
        distance = self.distance() / 1000

        return distance/total_elapsed_time

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