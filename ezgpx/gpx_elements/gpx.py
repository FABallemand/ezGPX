try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

import logging
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Union

import pandas as pd
import xmlschema

from ..utils import haversine_distance, ramer_douglas_peucker
from .extensions import Extensions
from .gpx_element import GpxElement
from .metadata import Metadata
from .route import Route
from .track import Track
from .way_point import WayPoint


class Gpx(GpxElement):
    """
    gpxType element in GPX file.
    """
    fields = ["version", "creator", "metadata",
              "wpt", "rte", "trk", "extensions"]
    mandatory_fields = ["version", "creator"]

    def __init__(
            self,
            tag: str = "gpx",
            version: str = None,
            creator: str = None,
            xsi_schema_location: List[str] = None,
            xmlns: Dict = None,
            metadata: Metadata = None,
            wpt: List[WayPoint] = None,
            rte: List[Route] = None,
            trk: List[Track] = None,
            extensions: Extensions = None) -> None:

        self.tag: str = tag
        self.version: str = version
        self.creator: str = creator
        if xsi_schema_location is None:
            self.xsi_schema_location: List[str] = []
        else:
            self.xsi_schema_location: List[str] = xsi_schema_location
        if xmlns is None:
            self.xmlns: Dict = {}
        else:
            self.xmlns: Dict = xmlns
        self.metadata: Metadata = metadata
        if wpt is None:
            self.wpt: List[WayPoint] = []
        else:
            self.wpt: List[WayPoint] = wpt
        if rte is None:
            self.rte: List[Route] = []
        else:
            self.rte: List[Route] = rte
        if trk is None:
            self.trk: List[Track] = []
        else:
            self.trk: List[Track] = trk
        self.extensions: Extensions = extensions

###############################################################################
#### Schemas ##################################################################
###############################################################################

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
                schema = xmlschema.XMLSchema(
                    files("ezgpx.schemas").joinpath("gpx_1_1/gpx.xsd"))
            elif self.version == "1.0":
                schema = xmlschema.XMLSchema(
                    files("ezgpx.schemas").joinpath("gpx_1_0/gpx.xsd"))
            else:
                logging.error(
                    "Unable to check XML schema (unsupported GPX version)")
                return False

        # KML
        elif file_path.endswith(".kml"):
            schema = xmlschema.XMLSchema(
                files("ezgpx.schemas").joinpath("kml_2_2/ogckml22.xsd"))

        # KMZ
        elif file_path.endswith(".kmz"):
            return False

        # FIT
        elif file_path.endswith(".fit"):
            logging.error(
                "Unable to check XML schema (fit files are not XML files)")
            return False

        # NOT SUPPORTED
        else:
            logging.error(
                "Unable to check XML schema (unable to identify file type)")
            return False

        if schema is not None:
            return schema.is_valid(file_path)
        else:
            logging.error(
                "Unable to check XML schema (unable to load XML schema)")
            return False

    def check_xml_extensions_schemas(self, file_path: str) -> bool:
        gpx_schemas = [
            s for s in self.xsi_schema_location if s.endswith(".xsd")]
        gpx_schemas.remove("http://www.topografix.com/GPX/1/1/gpx.xsd")
        for gpx_schema in gpx_schemas:
            logging.debug("schema = %s", gpx_schema)
            schema = xmlschema.XMLSchema(gpx_schema)
            if not schema.is_valid(file_path):
                logging.error("File does not follow %s", gpx_schema)
                return False

###############################################################################
#### Name #####################################################################
###############################################################################

    def name(self) -> str:
        """
        Return activity name.

        Returns
        -------
        str
            Activity name.
        """
        return self.trk[0].name

    def set_name(self, new_name: str) -> None:
        """
        Set name.

        Parameters
        ----------
        new_name : str
            New name.
        """
        self.trk[0].name = new_name

###############################################################################
#### Points ###################################################################
###############################################################################

    def nb_points(self) -> int:
        """
        Compute the number of points in the GPX.

        Returns
        -------
        int
            Number of points in the GPX.
        """
        nb_pts = 0
        for track in self.trk:
            for track_segment in track.trkseg:
                nb_pts += len(track_segment.trkpt)
        return nb_pts

    def bounds(self) -> Tuple[float, float, float, float]:
        """
        Find minimum and maximum latitude and longitude.

        Returns
        -------
        Tuple[float, float, float, float]
            Min latitude, min longitude, max latitude, max longitude.
        """
        min_lat = self.trk[0].trkseg[0].trkpt[0].lat
        min_lon = self.trk[0].trkseg[0].trkpt[0].lon
        max_lat = min_lat
        max_lon = min_lon

        for track in self.trk:
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

    def first_point(self) -> WayPoint:
        """
        Return GPX first point.

        Returns
        -------
        WayPoint
            First point.
        """
        return self.trk[0].trkseg[0].trkpt[0]

    def last_point(self) -> WayPoint:
        """
        Return GPX last point.

        Returns
        -------
        WayPoint
            Last point.
        """
        return self.trk[-1].trkseg[-1].trkpt[-1]

    def extreme_points(self) -> Tuple[WayPoint, WayPoint, WayPoint, WayPoint]:
        """
        Find extreme points in track, i.e.: points with lowest and highest latitude and longitude.

        Returns
        -------
        Tuple[WayPoint, WayPoint, WayPoint, WayPoint]
            Min latitude point, min longitude point, max latitude point, max longitude point
        """
        min_lat_point = self.trk[0].trkseg[0].trkpt[0]
        min_lon_point = self.trk[0].trkseg[0].trkpt[0]
        max_lat_point = self.trk[0].trkseg[0].trkpt[0]
        max_lon_point = self.trk[0].trkseg[0].trkpt[0]

        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.lat < min_lat_point.lat:
                        min_lat_point = track_point
                    if track_point.lon < min_lon_point.lon:
                        min_lon_point = track_point
                    if track_point.lat > max_lat_point.lat:
                        max_lat_point = track_point
                    if track_point.lon > max_lon_point.lon:
                        max_lon_point = track_point
        return min_lat_point, min_lon_point, max_lat_point, max_lon_point

###############################################################################
#### Distance and Elevation ###################################################
###############################################################################

    def distance(self) -> float:
        """
        Compute the total distance (meters) of tracks contained in the Gpx element.

        Returns
        -------
        float
            Distance (meters).
        """
        dst = 0.0
        previous_point = self.trk[0].trkseg[0].trkpt[0]
        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    dst += haversine_distance(previous_point, track_point)
                    previous_point = track_point
        return dst

    def compute_points_distance_from_start(self):
        """
        Compute distance from start at each point.
        """
        dst = 0.0
        previous_point = self.trk[0].trkseg[0].trkpt[0]
        previous_point.distance_from_start = dst
        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    dst += haversine_distance(previous_point, track_point)
                    track_point.distance_from_start = dst
                    previous_point = track_point

    def ascent(self) -> float:
        """
        Compute the total ascent (meters) of tracks contained in the Gpx element.

        Returns
        -------
        float
            Ascent (meters).
        """
        ascent = 0
        previous_elevation = self.trk[0].trkseg[0].trkpt[0].ele
        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ele > previous_elevation:
                        ascent += track_point.ele - previous_elevation
                    previous_elevation = track_point.ele
        return ascent

    def descent(self) -> float:
        """
        Compute the total descent (meters) of tracks contained in the Gpx element.

        Returns
        -------
        float
            Descent (meters).
        """
        descent = 0
        previous_elevation = self.trk[0].trkseg[0].trkpt[0].ele
        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ele < previous_elevation:
                        descent += previous_elevation - track_point.ele
                    previous_elevation = track_point.ele
        return descent

    def min_elevation(self) -> float:
        """
        Compute minimum elevation (meters) in tracks contained in the Gpx element.

        Returns
        -------
        float
            Minimum elevation (meters).
        """
        min_elevation = self.trk[0].trkseg[0].trkpt[0].ele
        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ele < min_elevation:
                        min_elevation = track_point.ele
        return min_elevation

    def max_elevation(self) -> float:
        """
        Compute maximum elevation (meters) in tracks contained in the Gpx element.

        Returns
        -------
        float
            Maximum elevation (meters).
        """
        max_elevation = self.trk[0].trkseg[0].trkpt[0].ele
        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ele > max_elevation:
                        max_elevation = track_point.ele
        return max_elevation

    def compute_points_ascent_rate(self) -> None:
        """
        Compute ascent rate at each point.
        """
        previous_point = self.first_point()

        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    distance = haversine_distance(previous_point, track_point)
                    ascent = track_point.ele - previous_point.ele
                    try:
                        track_point.ascent_rate = (ascent * 100) / distance
                        logging.debug(
                            f"distance={distance} | ascent={ascent} | ascent_rate={track_point.ascent_rate}")
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

        for track in self.trk:
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
        self.compute_points_ascent_rate()  # Check if it needs to be done

        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ascent_rate > max_ascent_rate:
                        max_ascent_rate = track_point.ascent_rate

        return max_ascent_rate

###############################################################################
#### Time #####################################################################
###############################################################################

    def utc_start_time(self) -> datetime:
        """
        Return the activity UTC start time.

        Returns
        -------
        datetime
            UTC start time.
        """
        return self.trk[0].trkseg[0].trkpt[0].time

    def utc_stop_time(self):
        """
        Return the activity UTC stop time.

        Returns
        -------
        datetime
            UTC stop time.
        """
        return self.trk[-1].trkseg[-1].trkpt[-1].time

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
            start_time = self.trk[0].trkseg[0].trkpt[0].time.replace(
                tzinfo=timezone.utc).astimezone(tz=None)
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
            stop_time = self.trk[-1].trkseg[-1].trkpt[-1].time.replace(
                tzinfo=timezone.utc).astimezone(tz=None)
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
        stopped_time = self.start_time() - self.start_time()  # Better way to do it?

        previous_point = self.trk[0].trkseg[0].trkpt[0]

        for track in self.trk:
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

###############################################################################
#### Speed and Pace ###########################################################
###############################################################################

    def avg_speed(self) -> float:
        """
        Compute the average speed (kilometres per hour) during the activity.

        Returns
        -------
        float
            Average speed (kilometres per hour).
        """
        # Compute and convert total elapsed time
        total_elapsed_time = self.total_elapsed_time()
        total_elapsed_time = total_elapsed_time.total_seconds() / 3600

        # Compute and convert distance
        distance = self.distance() / 1000

        return distance/total_elapsed_time

    def avg_moving_speed(self) -> float:
        """
        Compute the average moving speed (kilometres per hour) during the activity.

        Returns
        -------
        float
            Average moving speed (kilometres per hour).
        """
        # Compute and convert moving time
        moving_time = self.moving_time()
        moving_time = moving_time.total_seconds() / 3600

        # Compute and convert distance
        distance = self.distance() / 1000

        return distance / moving_time

    def compute_points_speed(self) -> None:
        """
        Compute speed (kilometres per hour) at each track point.
        """
        previous_point = self.first_point()

        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    distance = haversine_distance(
                        previous_point, track_point) / 1000  # Convert to kilometers
                    # Convert to hours
                    time = (track_point.time -
                            previous_point.time).total_seconds() / 3600
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

        for track in self.trk:
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

        for track in self.trk:
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

        for track in self.trk:
            for segment in track.trkseg:
                for point in segment.trkpt:
                    try:
                        point.pace = 60.0 / point.speed
                    except:
                        # Fill with average moving space (first point)
                        point.pace = self.avg_moving_pace()

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

        for track in self.trk:
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

        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.pace > max_pace:
                        max_pace = track_point.pace

        return max_pace

    def compute_points_ascent_speed(self) -> None:
        """
        Compute ascent speed (kilometres per hour) at each track point.
        """
        previous_point = self.first_point()

        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    ascent = (track_point.ele - previous_point.ele) / \
                        1000  # Convert to kilometers
                    # Convert to hours
                    time = (track_point.time -
                            previous_point.time).total_seconds() / 3600
                    try:
                        track_point.ascent_speed = ascent / time
                    except:
                        track_point.ascent_speed = 0.0
                    previous_point = track_point

    def min_ascent_speed(self) -> float:
        """
        Return the minimum ascent speed (kilometres per hour) during the activity.

        Returns
        -------
        float
            Minimum ascent speed.
        """
        min_ascent_speed = 1000.0
        self.compute_points_ascent_speed()

        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ascent_speed < min_ascent_speed:
                        min_ascent_speed = track_point.ascent_speed

        return min_ascent_speed

    def max_ascent_speed(self) -> float:
        """
        Return the maximum ascent speed (kilometres per hour) during the activity.

        Returns
        -------
        float
            Maximum ascent speed.
        """
        max_ascent_speed = -1.0
        self.compute_points_ascent_speed()

        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ascent_speed > max_ascent_speed:
                        max_ascent_speed = track_point.ascent_speed

        return max_ascent_speed

###############################################################################
#### Data Removal #############################################################
###############################################################################

    def remove_metadata(self):
        """
        Remove metadata.
        """
        self.metadata = None

    def remove_elevation(self):
        """
        Remove elevation data.
        """
        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    track_point.ele = None

    def remove_time(self):
        """
        Remove time data.
        """
        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    track_point.time = None

    def remove_extensions(self):
        """
        Remove extensions data.
        """
        # Remove extensions from gpx
        self.extensions = None

        # Remove extensions from metadata
        if self.metadata is not None:
            self.metadata.extensions = None

        # Remove extensions from waypoints
        if self.wpt is not None:
            for pt in self.wpt:
                pt.extensions = None

        # Remove extensions from routes
        if self.rte is not None:
            for rt in self.rte:
                rt.extensions = None

        # Remove extensions from tracks
        if self.trk is not None:
            for track in self.trk:
                track.extensions = None
                # Remove extensions from track segments
                if track.trkseg is not None:
                    for track_segment in track.trkseg:
                        track_segment.extensions = None
                        if track_segment.trkpt is not None:
                            for track_point in track_segment.trkpt:
                                # Remove extensions from track points
                                track_point.extensions = None

###############################################################################
#### Error Correction #########################################################
###############################################################################

    def remove_points(self, remove_factor: int = 2):
        count = 0
        for track in self.trk:
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

        for track in self.trk:
            for track_segment in track.trkseg:

                new_trkpt = []

                for track_point in track_segment.trkpt:
                    # GPS error
                    if previous_point is not None and haversine_distance(previous_point,
                                                                         track_point) > error_distance:
                        logging.warning(
                            "Point %s has been removed (GPS error)", track_point)
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

        for track in self.trk:
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

###############################################################################
#### Simplification ###########################################################
###############################################################################

    def simplify(self, epsilon):
        """
        Simplify GPX trk using Ramer-Douglas-Peucker algorithm.

        Parameters
        ----------
        epsilon : _type_
            Tolerance.
        """
        for track in self.trk:
            for segment in track.trkseg:
                segment.trkpt = ramer_douglas_peucker(segment.trkpt, epsilon)

###############################################################################
#### Exports ##################################################################
###############################################################################

    def to_dataframe(
            self,
            values: List[str] = None) -> pd.DataFrame:
        """
        Convert GPX object to Pandas Dataframe.
        Missing values are filled with default values (0 for elevation, empty string for time).

        Parameters
        ----------
        values : List[str], optional
            List of values to write, by default None
            Supported values: "lat", "lon", "ele", "time", "speed", "pace",
            "ascent_rate", "ascent_speed", "distance_from_start"

        Returns
        -------
        pd.DataFrame
            Dataframe containing data from GPX.
        """
        # Retrieve parameters
        if values is None:
            values = ["lat", "lon"]
        lat = "lat" in values
        lon = "lon" in values
        ele = "ele" in values
        time = "time" in values
        speed = "speed" in values
        pace = "pace" in values
        ascent_rate = "ascent_rate" in values
        ascent_speed = "ascent_speed" in values
        distance_from_start = "distance_from_start" in values

        # Compute required values
        test_point = self.first_point()
        if speed and test_point.speed is None:
            self.compute_points_speed()
        if pace and test_point.pace is None:
            self.compute_points_pace()
        if ascent_rate and test_point.ascent_rate is None:
            self.compute_points_ascent_rate()
        if ascent_speed and test_point.ascent_speed is None:
            self.compute_points_ascent_speed()
        if distance_from_start and test_point.distance_from_start is None:
            self.compute_points_distance_from_start()

        # Create dataframe
        route_info = []
        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    track_point_dict = {}
                    if lat:
                        track_point_dict["lat"] = track_point.lat
                    if lon:
                        track_point_dict["lon"] = track_point.lon
                    if ele:
                        if track_point.ele is not None:
                            track_point_dict["ele"] = track_point.ele
                        else:
                            track_point_dict["ele"] = 0
                    if time:
                        if track_point.time is not None:
                            track_point_dict["time"] = str(track_point.time.replace(
                                tzinfo=timezone.utc).astimezone(tz=None))
                        else:
                            track_point_dict["time"] = ""
                    if speed:
                        track_point_dict["speed"] = track_point.speed
                    if pace:
                        track_point_dict["pace"] = track_point.pace
                    if ascent_rate:
                        track_point_dict["ascent_rate"] = track_point.ascent_rate
                    if ascent_speed:
                        track_point_dict["ascent_speed"] = track_point.ascent_speed
                    if distance_from_start:
                        track_point_dict["distance_from_start"] = track_point.distance_from_start
                    route_info.append(track_point_dict)
        df = pd.DataFrame(route_info)
        return df

    def to_csv(
            self,
            path: str = None,
            values: List[str] = None,
            sep: str = ",",
            header: bool = True,
            index: bool = False) -> Union[str, None]:
        """
        Write the GPX object track coordinates to a .csv file.

        Parameters
        ----------
        path : str, optional
            Path to the .csv file, by default None
        values : List[str], optional
            List of values to write, by default None
            Supported values: "lat", "lon", "ele", "time", "speed", "pace",
            "ascent_rate", "ascent_speed", "distance_from_start"
        sep : str, optional
            Separator, by default ","
        header : bool, optional
            Toggle header, by default True
        index : bool, optional
             Toggle index, by default False

        Returns
        -------
        str
            CSV like string if path is set to None.
        """
        if values is None:
            values = ["lat", "lon"]

        # Argument columns is required for KML writer (keep values order)
        return self.to_dataframe(values).to_csv(path, sep=sep, columns=values, header=header, index=index)
