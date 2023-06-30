import logging
import pandas as pd
from datetime import datetime, timezone

from .metadata import *
from .track import *

from ..utils import haversine_distance, ramer_douglas_peucker

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
        self.tracks: list[Track] = tracks

    def distance(self) -> float:
        """
        Compute the total distance (meters) of the tracks contained in the Gpx element.

        Returns:
            float: Distance (meters)
        """
        dst = 0
        previous_point = self.tracks[0].trkseg[0].trkpt[0]
        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    dst += haversine_distance(previous_point, track_point)
                    previous_point = track_point
        return dst
    
    def ascent(self) -> float:
        """
        Compute the total ascent (meters) of the tracks contained in the Gpx element.

        Returns:
            float: Ascent (meters)
        """
        ascent = 0
        previous_elevation = self.tracks[0].trkseg[0].trkpt[0].elevation
        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
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
        previous_elevation = self.tracks[0].trkseg[0].trkpt[0].elevation
        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
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
        min_elevation = self.tracks[0].trkseg[0].trkpt[0].elevation
        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.elevation < min_elevation:
                        min_elevation = track_point.elevation
        return min_elevation
    
    def max_elevation(self) -> float:
        """
        Compute maximum elevation (meters) in the tracks contained in the Gpx element.

        Returns:
            float: Maximum elevation (meters).
        """
        max_elevation = self.tracks[0].trkseg[0].trkpt[0].elevation
        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.elevation > max_elevation:
                        max_elevation = track_point.elevation
        return max_elevation
    
    def utc_start_time(self) -> datetime:
        """
        Return the activity UTC starting time.

        Returns:
            datetime: UTC start time.
        """
        return self.tracks[0].trkseg[0].trkpt[0].time
    
    def utc_stop_time(self):
        """
        Return the activity UTC stopping time.

        Returns:
            datetime: UTC stop time.
        """
        return self.tracks[-1].trkseg[-1].trkpt[-1].time
    
    def start_time(self) -> datetime:
        """
        Return the activity starting time.

        Returns:
            datetime: Start time.
        """
        return self.tracks[0].trkseg[0].trkpt[0].time.replace(tzinfo=timezone.utc).astimezone(tz=None) 
    
    def stop_time(self):
        """
        Return the activity stopping time.

        Returns:
            datetime: Stop time.
        """
        return self.tracks[-1].trkseg[-1].trkpt[-1].time.replace(tzinfo=timezone.utc).astimezone(tz=None)
    
    def total_elapsed_time(self) -> datetime:
        """
        Compute the total elapsed time.

        Returns:
            datetime: Total elapsed time.
        """
        return self.stop_time() - self.start_time()
    
    def stopped_time(self, tolerance: float = 2.45) -> datetime:
        """
        Compute the stopped time during activity.

        Args:
            tolerance (float, optional): Maximal distance between two points for movement. Defaults to 2.45. (According to my tests with strava_run_1 and the data on Strava).

        Returns:
            datetime: Stopped time.
        """
        stopped_time = self.start_time() - self.start_time() # Better way to do it?

        previous_point = self.tracks[0].trkseg[0].trkpt[0]

        for track in self.tracks:
            for segment in track.trkseg:
                for point in segment.trkpt:
                    if haversine_distance(previous_point, point) < tolerance:
                        stopped_time += point.time - previous_point.time
                    previous_point = point

        return stopped_time
    
    def moving_time(self) -> datetime:
        """
        Compute the moving time during the activity.

        Returns:
            datetime: Moving time.
        """
        return self.total_elapsed_time() - self.stopped_time()
    
    def avg_speed(self) -> float:
        """
        Compute the average speed (kilometers per hour) during the activity.

        Returns:
            float: Average speed (kilometers per hour).
        """
        # Compute and convert total elapsed time
        total_elapsed_time = self.total_elapsed_time()
        total_elapsed_time = total_elapsed_time.total_seconds() / 3600

        # Compute and convert distance
        distance = self.distance() / 1000

        return distance/total_elapsed_time
    
    def avg_moving_speed(self) -> float:
        """
        Compute the average moving speed (kilometers per hour) during the activity.

        Returns:
            float: Average moving speed (kilometers per hour).
        """
        # Compute and convert moving time
        moving_time = self.moving_time()
        moving_time = moving_time.total_seconds() / 3600

        # Compute and convert distance
        distance = self.distance() / 1000

        return distance / moving_time
    
    def avg_pace(self) -> float:
        """
        Compute the average pace (minute per kilometer) during the activity.

        Returns:
            float: Average pace (minute per kilometer).
        """
        return 60 / self.avg_speed()
    
    def avg_moving_pace(self) -> float:
        """
        Compute the average moving pace (minute per kilometer) during the activity.

        Returns:
            float: Average moving pace (minute per kilometer).
        """
        return 60 / self.avg_moving_speed()

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert Gpx element to Pandas Dataframe.

        Returns:
            pd.DataFrame: Dataframe containing position data from GPX.
        """
        route_info = []
        for track in self.tracks:
            for segment in track.trkseg:
                for point in segment.trkpt:
                    route_info.append({
                        "latitude": point.latitude,
                        "longitude": point.longitude,
                        "elevation": point.elevation,
                        "x": point._x,
                        "y": point._y
                    })
        df = pd.DataFrame(route_info)
        return df
    
    def project(self):
        for track in self.tracks:
            track.project()
    
    def remove_gps_errors(self, error_distance=100):
        """
        Remove GPS errors.

        Args:
            error_distance (int, optional): Error threshold distance (meters) between two points. Defaults to 1000.

        Returns:
            list: List of removed points (GPS errors).
        """
        previous_point = None
        gps_errors = []

        for track in self.tracks:
            for track_segment in track.trkseg:

                new_trkpt = []

                for track_point in track_segment.trkpt:
                    # GPS error
                    if previous_point is not None and haversine_distance(previous_point,
                                                                         track_point) > error_distance:
                        logging.warning(f"Point {track_point} has been removed (GPS error)")
                        gps_errors.append(track_point)
                    # No GPS error
                    else:
                        new_trkpt.append(track_point)
                        previous_point = track_point

                track_segment.trkpt = new_trkpt

        return gps_errors
    
    def remove_close_points(self, min_dist: float = 1, max_dist: float = 10):
        """
        Remove points that are to close together.

        Args:
            min_dist (float, optional): Minimal distance between two points. Defaults to 1.
            max_dist (float, optional): Maximal distance between two points. Defaults to 10.
        """
        point_1 = None
        point_2 = None
        
        for track in self.tracks:
            for segment in track.trkseg:

                new_trkpt = []

                for point in segment.trkpt:
                    if point_1 is None:
                        point_1 = point
                        new_trkpt.append(point_1)
                    elif point_2 is None:
                        point_2 = point
                    else:
                        if ((haversine_distance(point_1, point_2) < min_dist
                             or haversine_distance(point_2, point) < min_dist)
                            and haversine_distance(point_1, point) < max_dist):
                            point_2 = point
                        else:
                            new_trkpt.append(point_2)
                            point_1 = point_2
                            point_2 = point

                segment.trkpt = new_trkpt

    def remove_points(self, remove_factor: int = 2):
        count = 0
        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if count % remove_factor == 0:
                        track_segment.trkpt.remove(track_point)
                        count += 1

    def simplify(self, epsilon):
        """
        Simplify GPX tracks using Ramer-Douglas-Peucker algorithm.

        Args:
            epsilon (float): Tolerance.
        """
        for track in self.tracks:
            for segment in track.trkseg:
                segment.trkpt = ramer_douglas_peucker(segment.trkpt, epsilon)