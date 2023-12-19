import os
from importlib_resources import files
from typing import Union, List, Tuple
import logging
import xmlschema
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
            xsi_schema_location: List[str] = None,
            xmlns_gpxtpx: str = None,
            xmlns_gpxx: str = None,
            xmlns_gpxtrk: str = None,
            xmlns_wptx1: str = None,
            metadata: Metadata = None,
            wpt: List[WayPoint] = None,
            rte: List[Route] = None,
            tracks: List[Track] = None,
            extensions: Extensions = None) -> None:
        """
        Initialize Gpx instance.

        Parameters
        ----------
        tag : str, optional
            XML tag, by default "gpx"
        creator : str, optional
            Creator, by default None
        xmlns : str, optional
            XML xmlns, by default None
        version : str, optional
            Version, by default None
        xmlns_xsi : str, optional
            XML xmlns_xsi, by default None
        xsi_schema_location : List[str], optional
            XML schema location, by default None
        xmlns_gpxtpx : str, optional
            ???, by default None
        xmlns_gpxx : str, optional
            ???, by default None
        xmlns_gpxtrk : str, optional
            ???, by default None
        xmlns_wptx1 : str, optional
            ???, by default None
        metadata : Metadata, optional
            Metadata, by default None
        wpt : List[WayPoint], optional
            Way points, by default None
        rte : List[Route], optional
            Routes, by default None
        tracks : List[Track], optional
            List of tracks, by default None
        extensions : Extensions, optional
            Extensions, by default None
        """
        self.tag: str = tag
        self.creator: str = creator
        self.xmlns: str = xmlns
        self.version: str = version

        self.xmlns_xsi: str = xmlns_xsi
        if xsi_schema_location is None:
            self.xsi_schema_location: str = []
        else:
            self.xsi_schema_location: str = xsi_schema_location
        self.xmlns_gpxtpx: str = xmlns_gpxtpx
        self.xmlns_gpxx: str = xmlns_gpxx
        self.xmlns_gpxtrk: str = xmlns_gpxtrk
        self.xmlns_wptx1: str = xmlns_wptx1

        self.metadata: Metadata = metadata
        if wpt is None:
            self.wpt:List[WayPoint] = []
        else:
            self.wpt:List[WayPoint] = wpt
        if rte is None:
            self.rte: List[Route] = []
        else:
            self.rte: List[Route] = rte
        if tracks is None:
            self.tracks: List[Track] = []
        else:
            self.tracks: List[Track] = tracks
        self.extensions: Extensions = extensions

    def check_xml_schema(self, file_path: str) -> bool:
        """
        Check XML schema.

        Parameters
        ----------
        file_path : str
            File path

        Returns
        -------
        bool
            True if the file follows XML schemas
        """
        schema = None

        # GPX
        if file_path.endswith(".gpx"):
            if self.version == "1.1":
                schema = xmlschema.XMLSchema(files("ezgpx.schemas").joinpath("gpx_1_1/gpx.xsd"))
            elif self.version == "1.0":
                schema = xmlschema.XMLSchema(files("ezgpx.schemas").joinpath("gpx_1_0/gpx.xsd"))
            else:
                logging.error("Unable to check XML schema (unsupported GPX version)")
                return False

        # KML
        elif file_path.endswith(".kml"):
            schema = xmlschema.XMLSchema(files("ezgpx.schemas").joinpath("kml_2_2/ogckml22.xsd"))

        # KMZ
        elif file_path.endswith(".kmz"):
            return False

        # FIT
        elif file_path.endswith(".fit"):
            logging.error("Unable to check XML schema (fit files are not XML files)")
            return False
        
        # NOT SUPPORTED
        else:
            logging.error("Unable to check XML schema (unable to identify file type)")
            return False

        if schema is not None:
            return schema.is_valid(file_path)
        else:
            logging.error("Unable to check XML schema (unable to load XML schema)")
            return False
            
    def check_xml_extensions_schemas(self, file_path: str) -> bool:
        gpx_schemas = [s for s in self.xsi_schema_location if s.endswith(".xsd")]
        for gpx_schema in gpx_schemas:
            logging.debug(f"schema = {gpx_schema}")
            schema = xmlschema.XMLSchema(gpx_schema)
            if not schema.is_valid(file_path):
                logging.error(f"File does not follow {gpx_schema}")
                return False

    def name(self) -> str:
        """
        Return activity name.

        Returns
        -------
        str
            Activity name.
        """
        return self.tracks[0].name
    
    def set_name(self, new_name: str) -> None:
        """
        Set name.

        Parameters
        ----------
        new_name : str
            New name.
        """
        self.tracks[0].name = new_name

    def nb_points(self) -> int:
        """
        Compute the number of points in the GPX.

        Returns
        -------
        int
            Number of points in the GPX.
        """
        nb_pts = 0
        for track in self.tracks:
            for track_segment in track.trkseg:
                nb_pts += len(track_segment.trkpt)
        return nb_pts
    
    def first_point(self) -> WayPoint:
        """
        Return GPX first point.

        Returns
        -------
        WayPoint
            First point.
        """
        return self.tracks[0].trkseg[0].trkpt[0]

    def last_point(self) -> WayPoint:
        """
        Return GPX last point.

        Returns
        -------
        WayPoint
            Last point.
        """
        return self.tracks[-1].trkseg[-1].trkpt[-1]
    
    def bounds(self) -> Tuple[float, float, float, float]:
        """
        Find minimum and maximum latitude and longitude.

        Returns
        -------
        Tuple[float, float, float, float]
            Min latitude, min longitude, max latitude, max longitude.
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


    def center(self) -> Tuple[float, float]:
        """
        Compute the center coordinates of the track.

        Returns
        -------
        Tuple[float, float]
            Latitude and longitude of the center point.
        """
        min_lat, min_lon, max_lat, max_lon = self.bounds()
        center_lat = min_lat + (max_lat - min_lat) / 2
        center_lon = min_lon + (max_lon - min_lon) / 2
        return center_lat, center_lon

    def distance(self) -> float:
        """
        Compute the total distance (meters) of the tracks contained in the Gpx element.

        Returns
        -------
        float
            Distance (meters).
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

        Returns
        -------
        float
            Ascent (meters).
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

        Returns
        -------
        float
            Descent (meters).
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
    
    def compute_points_ascent_rate(self) -> None:
        """
        Compute ascent rate at each point.
        """
        previous_point = self.first_point()

        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    distance = haversine_distance(previous_point, track_point)
                    ascent = track_point.ele - previous_point.ele
                    try:
                        track_point.ascent_rate = (ascent * 100) / distance
                        logging.debug(f"distance={distance} | ascent={ascent} | ascent_rate={track_point.ascent_rate}")
                    except:
                        track_point.ascent_rate = 0.0
                    previous_point = track_point

    def min_ascent_rate(self) -> float:
        """
        Return activity minimum ascent rate.

        Returns
        -------
        float
            Minimum ascent rate.
        """
        min_ascent_rate = 100.0
        self.compute_points_ascent_rate()

        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ascent_rate < min_ascent_rate:
                        min_ascent_rate = track_point.ascent_rate

        return min_ascent_rate 

    def max_ascent_rate(self) -> float:
        """
        Return activity maximum ascent rate.

        Returns
        -------
        float
            Maximum ascent rate.
        """
        max_ascent_rate = -1.0
        self.compute_points_ascent_rate()

        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ascent_rate > max_ascent_rate:
                        max_ascent_rate = track_point.ascent_rate

        return max_ascent_rate                
    
    def min_elevation(self) -> float:
        """
        Compute minimum elevation (meters) in the tracks contained in the Gpx element.

        Returns
        -------
        float
            Minimum elevation (meters).
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

        Returns
        -------
        float
            Maximum elevation (meters).
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
        Return the activity UTC start time.

        Returns
        -------
        datetime
            UTC start time.
        """
        return self.tracks[0].trkseg[0].trkpt[0].time
    
    def utc_stop_time(self):
        """
        Return the activity UTC stop time.

        Returns
        -------
        datetime
            UTC stop time.
        """
        return self.tracks[-1].trkseg[-1].trkpt[-1].time
    
    def start_time(self) -> datetime:
        """
        Return the activity start time.

        Returns
        -------
        datetime
            Start time.
        """
        start_time = None
        try:
            start_time = self.tracks[0].trkseg[0].trkpt[0].time.replace(tzinfo=timezone.utc).astimezone(tz=None) 
        except:
            logging.error("Unable to find activity start time")
        return start_time
    
    def stop_time(self) -> datetime:
        """
        Return the activity stop time.

        Returns
        -------
        datetime
            Stop time.
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

        Returns
        -------
        datetime
            Total elapsed time.
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

        Parameters
        ----------
        tolerance : float, optional
            Maximal distance between two points for movement, by default 2.45
            (According to my tests with strava_run_1.gpx and the data on Strava)

        Returns
        -------
        datetime
            Stopped time.
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

        Returns
        -------
        datetime
            Moving time.
        """
        return self.total_elapsed_time() - self.stopped_time()
    
    def avg_speed(self) -> float:
        """
        Compute the average speed (kilometers per hour) during the activity.

        Returns
        -------
        float
            Average speed (kilometers per hour).
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

        Returns
        -------
        float
            Average moving speed (kilometers per hour).
        """
        # Compute and convert moving time
        moving_time = self.moving_time()
        moving_time = moving_time.total_seconds() / 3600

        # Compute and convert distance
        distance = self.distance() / 1000

        return distance / moving_time
    
    def compute_points_speed(self) -> None:
        """
        Compute speed (kilometers per hour) at each track point.
        """
        previous_point = self.first_point()

        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    distance = haversine_distance(previous_point, track_point) / 1000 # Convert to kilometers
                    time = (track_point.time - previous_point.time).total_seconds() / 3600 # Convert to hours
                    try:
                        track_point.speed = distance / time
                    except:
                        track_point.speed = 0.0
                    previous_point = track_point

    def min_speed(self) -> float:
        """
        Return the minimum speed during the activity.

        Returns
        -------
        float
            Minimum speed.
        """
        min_speed = 1000.0
        self.compute_points_speed()

        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.speed < min_speed:
                        min_speed = track_point.speed

        return min_speed

    def max_speed(self) -> float:
        """
        Return the maximum speed during the activity.

        Returns
        -------
        float
            Maximum speed.
        """
        max_speed = -1.0
        self.compute_points_speed()

        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.speed > max_speed:
                        max_speed = track_point.speed

        return max_speed
    
    def avg_pace(self) -> float:
        """
        Compute the average pace (minute per kilometer) during the activity.

        Returns
        -------
        float
            Average pace (minute per kilometer).
        """
        return 60.0 / self.avg_speed()
    
    def avg_moving_pace(self) -> float:
        """
        Compute the average moving pace (minute per kilometer) during the activity.

        Returns
        -------
        float
            Average moving pace (minute per kilometer).
        """
        return 60.0 / self.avg_moving_speed()
    
    def compute_points_pace(self) -> None:
        """
        Compute pace at each track point.
        """
        self.compute_points_speed()

        for track in self.tracks:
            for segment in track.trkseg:
                for point in segment.trkpt:
                    try:
                        point.pace = 60.0 / point.speed
                    except:
                        point.pace = self.avg_moving_pace() # Fill with average moving space (first point)

    def min_pace(self) -> float:
        """
        Return the minimum pace during the activity.

        Returns
        -------
        float
            Minimum pace.
        """
        min_pace = 1000.0
        self.compute_points_pace()

        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.pace < min_pace:
                        min_pace = track_point.pace

        return min_pace

    def max_pace(self) -> float:
        """
        Return the maximum pace during the activity.

        Returns
        -------
        float
            Maximum pace.
        """
        max_pace = -1.0
        self.compute_points_pace()

        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.pace > max_pace:
                        max_pace = track_point.pace

        return max_pace
    
    def compute_points_ascent_speed(self) -> None:
        """
        Compute ascent speed (kilometers per hour) at each track point.
        """
        previous_point = self.first_point()

        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    ascent = (track_point.ele - previous_point.ele) / 1000 # Convert to kilometers
                    time = (track_point.time - previous_point.time).total_seconds() / 3600 # Convert to hours
                    try:
                        track_point.ascent_speed = ascent / time
                    except:
                        track_point.ascent_speed = 0.0
                    previous_point = track_point

    def min_ascent_speed(self) -> float:
        """
        Return the minimum ascent speed (kilometers per hour) during the activity.

        Returns
        -------
        float
            Minimum ascent speed.
        """
        min_ascent_speed = 1000.0
        self.compute_points_ascent_speed()

        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ascent_speed < min_ascent_speed:
                        min_ascent_speed = track_point.ascent_speed

        return min_ascent_speed

    def max_ascent_speed(self) -> float:
        """
        Return the maximum ascent speed (kilometers per hour) during the activity.

        Returns
        -------
        float
            Maximum ascent speed.
        """
        max_ascent_speed = -1.0
        self.compute_points_ascent_speed()

        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ascent_speed > max_ascent_speed:
                        max_ascent_speed = track_point.ascent_speed

        return max_ascent_speed
    
    def remove_points(self, remove_factor: int = 2):
        count = 0
        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if count % remove_factor == 0:
                        track_segment.trkpt.remove(track_point)
                        count += 1

    def remove_gps_errors(self, error_distance=100):
        """
        Remove GPS errors.

        Parameters
        ----------
        error_distance : int, optional
            Error threshold distance (meters) between two points, by default 100

        Returns
        -------
        _type_
            List of removed points (GPS errors).
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

        Parameters
        ----------
        min_dist : float, optional
            Minimal distance between two points, by default 1
        max_dist : float, optional
            Maximal distance between two points, by default 10
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

    def simplify(self, epsilon):
        """
        Simplify GPX tracks using Ramer-Douglas-Peucker algorithm.

        Parameters
        ----------
        epsilon : _type_
            Tolerance.
        """
        for track in self.tracks:
            for segment in track.trkseg:
                segment.trkpt = ramer_douglas_peucker(segment.trkpt, epsilon)

    def to_dataframe(
            self,
            projection: bool = False,
            elevation: bool = True,
            speed: bool = False,
            pace: bool = False,
            ascent_rate: bool = False,
            ascent_speed: bool = False) -> pd.DataFrame:
        """
        Convert GPX object to Pandas Dataframe.

        Parameters
        ----------
        projection : bool, optional
            Toggle projection, by default False
        elevation : bool, optional
            Toggle elevation, by default True
        speed : bool, optional
            Toggle speed, by default False
        pace : bool, optional
            Toggle pace, by default False
        ascent_rate : bool, optional
            Toggle ascent rate, by default False
        ascent_speed : bool, optional
            Toggle ascent speed, by default False

        Returns
        -------
        pd.DataFrame
            Dataframe containing data from GPX.
        """
        test_point = self.first_point()
        if projection and test_point._x is None:
            logging.warning(f"Converting GPX to dataframe with missing projection data.")
        if speed and test_point.speed is None:
            self.compute_points_speed()
        if pace and test_point.pace is None:
            self.compute_points_pace()
        if ascent_rate and test_point.ascent_rate is None:
            self.compute_points_ascent_rate()
        if ascent_speed and test_point.ascent_speed is None:
            self.compute_points_ascent_speed()

        route_info = []
        for track in self.tracks:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    track_point_dict = {
                        "lat": track_point.lat,
                        "lon": track_point.lon
                    }
                    if elevation:
                        if track_point.ele is not None:
                            track_point_dict["ele"] = track_point.ele
                        else:
                            track_point_dict["ele"] = 0
                    if projection:
                        track_point_dict["x"] = track_point._x
                        track_point_dict["y"] = track_point._y
                    if speed:
                        track_point_dict["speed"] = track_point.speed
                    if pace:
                        track_point_dict["pace"] = track_point.pace
                    if ascent_rate:
                        track_point_dict["ascent_rate"] = track_point.ascent_rate
                    if ascent_speed:
                        track_point_dict["ascent_speed"] = track_point.ascent_speed
                    route_info.append(track_point_dict)
        df = pd.DataFrame(route_info)
        return df
    
    def to_csv(
            self,
            path: str = None,
            sep: str = ",",
            columns: List[str] = None,
            header: bool = True,
            index: bool = False) -> Union[str, None]:
        """
        Write the GPX object track coordinates to a .csv file.

        Parameters
        ----------
        path : str, optional
            Path to the .csv file, by default None
        sep : str, optional
            Separator, by default ","
        columns : List[str], optional
            List of columns to write, by default None
        header : bool, optional
            Toggle header, by default True
        index : bool, optional
             Toggle index, by default False

        Returns
        -------
        str
            CSV like string if path is set to None.
        """
        if columns is None:
            columns =  ["lat", "lon"]

        elevation = False
        projection = False
        speed = False
        pace = False
        ascent_rate = False
        ascent_speed = False
        
        if "ele" in columns:
            elevation = True
        if "x" in columns or "y" in columns:
            projection = True
        if "speed" in columns:
            speed = True
        if "pace" in columns:
            pace = True
        if "ascent_rate" in columns:
            ascent_rate = True
        if "ascent_speed" in columns:
            ascent_speed = True

        return self.to_dataframe(projection, elevation, speed, pace, ascent_rate, ascent_speed).to_csv(path, sep=sep, columns=columns, header=header, index=index)

    def project(self, projection: str):
        """
        Project tracks.

        Parameters
        ----------
        projection : str
            Projection.
        """
        for track in self.tracks:
            track.project(projection)