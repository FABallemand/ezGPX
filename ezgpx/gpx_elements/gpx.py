import logging
import pandas as pd
from datetime import datetime, timezone

from .metadata import Metadata
from .way_point import WayPoint
from .route import Route
from .track import Track
from .extensions import Extensions
from ..utils import haversine_distance, ramer_douglas_peucker

class Gpx():
    """
    gpxType element in GPX file.
    """

    def __init__(
            self,
            tag: str = "gpx",
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
            wpt: list[WayPoint] = [],
            rte: list[Route] = [],
            tracks: list[Track] = [],
            extensions: Extensions = None) -> None:
        """
        Initialize Gpx instance.

        Args:
            tag (str, optional): XML tag. Defaults to "gpx".
            creator (str, optional): Creator. Defaults to None.
            xmlns (str, optional): XML xmlns. Defaults to None.
            version (str, optional): Version. Defaults to None.
            xmlns_xsi (str, optional): XML xmlns_xsi. Defaults to None.
            xsi_schema_location (list[str], optional): XML schema location. Defaults to None.
            xmlns_gpxtpx (str, optional): _description_. Defaults to None.
            xmlns_gpxx (str, optional): _description_. Defaults to None.
            xmlns_gpxtrk (str, optional): _description_. Defaults to None.
            xmlns_wptx1 (str, optional): _description_. Defaults to None.
            metadata (Metadata, optional): Metadata. Defaults to None.
            wpt (list[WayPoint], optional): Way points. Defaults to [].
            rte (list[Route], optional): Routes. Defaults to [].
            tracks (list[Track], optional): List of tracks. Defaults to [].
            extensions (Extensions, optional): Extensions. Defaults to [].
        """
        self.tag: str = tag
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
        self.wpt:list[WayPoint] = wpt
        self.rte: list[Route] = rte
        self.tracks: list[Track] = tracks
        self.extensions: Extensions = extensions

    def name(self) -> str:
        """
        Return activity name.

        Returns:
            str: Activity name.
        """
        return self.tracks[0].name

    def nb_points(self) -> int:
        """
        Compute the number of points in the GPX.

        Returns:
            int: Number of points in the GPX.
        """
        nb_pts = 0
        for track in self.tracks:
            for track_segment in track.trkseg:
                nb_pts += len(track_segment.trkpt)
        return nb_pts
    
    def bounds(self) -> tuple[float, float, float, float]:
        """
        Find minimum and maximum latitude and longitude.

        Returns:
            tuple[float, float, float, float]: Min latitude, min longitude, max latitude, max longitude
        """
        min_lat = self.tracks[0].trkseg[0].trkpt[0].lat
        min_lon = self.tracks[0].trkseg[0].trkpt[0].lon
        max_lat = min_lat
        max_lon = min_lon

        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.lat < min_lat:
                        min_lat = track_point.lat
                    if track_point.lon < min_lon:
                        min_lon = track_point.lon
                    if track_point.lat > max_lat:
                        max_lat = track_point.lat
                    if track_point.lon > max_lon:
                        max_lon = track_point.lon
        return min_lat, min_lon, max_lat, max_lon


    def center(self) -> tuple[float, float]:
        """
        Compute the center coordinates of the track.

        Returns:
            tuple[float, float]: Latitude and longitude of the center point.
        """
        min_lat, min_lon, max_lat, max_lon = self.bounds()
        center_lat = min_lat + (max_lat - min_lat) / 2
        center_lon = min_lon + (max_lon - min_lon) / 2
        return center_lat, center_lon

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
        previous_elevation = self.tracks[0].trkseg[0].trkpt[0].ele
        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ele > previous_elevation:
                        ascent += track_point.ele - previous_elevation
                    previous_elevation = track_point.ele
        return ascent
    
    def descent(self) -> float:
        """
        Compute the total descent (meters) of the tracks contained in the Gpx element.

        Returns:
            float: Descent (meters)
        """
        descent = 0
        previous_elevation = self.tracks[0].trkseg[0].trkpt[0].ele
        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ele < previous_elevation:
                        descent += previous_elevation - track_point.ele
                    previous_elevation = track_point.ele
        return descent
    
    def min_elevation(self) -> float:
        """
        Compute minimum elevation (meters) in the tracks contained in the Gpx element.

        Returns:
            float: Minimum elevation (meters).
        """
        min_elevation = self.tracks[0].trkseg[0].trkpt[0].ele
        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ele < min_elevation:
                        min_elevation = track_point.ele
        return min_elevation
    
    def max_elevation(self) -> float:
        """
        Compute maximum elevation (meters) in the tracks contained in the Gpx element.

        Returns:
            float: Maximum elevation (meters).
        """
        max_elevation = self.tracks[0].trkseg[0].trkpt[0].ele
        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ele > max_elevation:
                        max_elevation = track_point.ele
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
        start_time = None
        try:
            start_time = self.tracks[0].trkseg[0].trkpt[0].time.replace(tzinfo=timezone.utc).astimezone(tz=None) 
        except:
            logging.error("Unable to find activity start time")
        return start_time
    
    def stop_time(self) -> datetime:
        """
        Return the activity stopping time.

        Returns:
            datetime: Stop time.
        """
        stop_time = None
        try:
            stop_time = self.tracks[-1].trkseg[-1].trkpt[-1].time.replace(tzinfo=timezone.utc).astimezone(tz=None)
        except:
            logging.error("Unable to find activity stop time")
        return stop_time
    
    def total_elapsed_time(self) -> datetime:
        """
        Compute the total elapsed time.

        Returns:
            datetime: Total elapsed time.
        """
        total_elapsed_time = None
        try:
            total_elapsed_time = self.stop_time() - self.start_time()
        except:
            logging.error("Unable to compute activity total elapsed time")
        return total_elapsed_time
    
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
                        "latitude": point.lat,
                        "longitude": point.lon,
                        "elevation": point.ele,
                        "x": point._x,
                        "y": point._y
                    })
        df = pd.DataFrame(route_info)
        return df
    
    def project(self, projection: str):
        """
        Project tracks.

        Args:
            projection (str): Projection.
        """
        for track in self.tracks:
            track.project(projection)
    
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