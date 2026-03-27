"""
This module contains the Gpx class.
"""

from __future__ import annotations

import io
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import IO, Any, Optional, Tuple

import narwhals as nw
import pandas as pd
import polars as pl
from narwhals.typing import IntoFrameT

from ..utils import haversine_distance, ramer_douglas_peucker
from .extensions import Extensions
from .gpx_element import GpxElement
from .metadata import Metadata
from .route import Route
from .track import Track
from .track_segment import TrackSegment
from .waypoint import WayPoint


class Gpx(GpxElement):
    """
    gpxType element in GPX file.
    """

    fields = ["version", "creator", "metadata", "wpt", "rte", "trk", "extensions"]
    mandatory_fields = ["version", "creator"]

    def __init__(
        self,
        *,
        tag: str = "gpx",
        version: str = None,
        creator: str = None,
        xsi_schema_location: list[str] = None,
        xmlns: dict = None,
        metadata: Metadata = None,
        wpt: list[WayPoint] = None,
        rte: list[Route] = None,
        trk: list[Track] = None,
        extensions: Extensions = None,
    ) -> None:
        """
        Initialise Gpx instance.

        Args:
            tag (str, optional): XML tag. Defaults to "gpx".
            version (str, optional): GPX schema version. Defaults to None.
            creator (str, optional): Creator. Defaults to None.
            xsi_schema_location (list[str], optional): XML schema
                instance. Defaults to None.
            xmlns (dict, optional): XML name spaces. Defaults to None.
            metadata (Metadata, optional): Metadata. Defaults to None.
            wpt (list[WayPoint], optional): List of waypoints. Defaults to None.
            rte (list[Route], optional): List of routes. Defaults to None.
            trk (list[Track], optional): List of tracks. Defaults to None.
            extensions (Extensions, optional): Extensions. Defaults to None.
        """
        self.tag: str = tag
        self.version: str = version
        self.creator: str = creator
        self.xsi_schema_location: list[str] = (
            [] if xsi_schema_location is None else xsi_schema_location
        )
        self.xmlns: dict = {} if xmlns is None else xmlns
        self.metadata: Metadata = metadata
        self.wpt: list[WayPoint] = [] if wpt is None else wpt
        self.rte: list[Route] = [] if rte is None else rte
        self.trk: list[Track] = [] if trk is None else trk
        self.extensions: Extensions = extensions

    @staticmethod
    def from_dataframe(df: IntoFrameT) -> Gpx:
        """
        Initialize Gpx from dataframe.

        Args:
            df (IntoFrameT): Dataframe with "lat", "lon" columns. Also
                supports "ele", "time" columns.
        """
        df = nw.from_native(df)

        trkpt = [
            WayPoint(
                tag="trkpt",
                lat=row["lat"],
                lon=row["lon"],
                ele=row.get("ele"),
                time=row.get("time"),
            )
            for row in df.iter_rows(named=True)
        ]
        trkseg = TrackSegment(trkpt=trkpt)
        trk = Track(trkseg=[trkseg])
        return Gpx(trk=[trk])

    ###############################################################################
    #### Name #####################################################################
    ###############################################################################

    def name(self) -> str:
        """
        Return activity name.
        """
        return self.trk[0].name

    def set_name(self, new_name: str) -> None:
        """
        Set name.

        Args:
            new_name (str): New name.
        """
        self.trk[0].name = new_name

    ###############################################################################
    #### Points ###################################################################
    ###############################################################################

    def nb_points(self) -> int:
        """
        Return the number of points in the GPX.
        """
        nb_pts = 0
        for track in self.trk:
            for track_segment in track.trkseg:
                nb_pts += len(track_segment.trkpt)
        return nb_pts

    def bounds(self) -> Tuple[float, float, float, float]:
        """
        Find minimum and maximum latitude and longitude.

        Returns:
            Tuple[float, float, float, float]: Min latitude, min
                longitude, max latitude, max longitude.
        """
        min_lat = self.trk[0].trkseg[0].trkpt[0].lat
        min_lon = self.trk[0].trkseg[0].trkpt[0].lon
        max_lat = min_lat
        max_lon = min_lon

        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    min_lat = min(min_lat, track_point.lat)
                    min_lon = min(min_lon, track_point.lon)
                    max_lat = max(max_lat, track_point.lat)
                    max_lon = max(max_lon, track_point.lon)
        return min_lat, min_lon, max_lat, max_lon

    def center(self) -> Tuple[float, float]:
        """
        Return latitude and longitude of the center point.
        """
        min_lat, min_lon, max_lat, max_lon = self.bounds()
        center_lat = min_lat + (max_lat - min_lat) / 2
        center_lon = min_lon + (max_lon - min_lon) / 2
        return center_lat, center_lon

    def first_point(self) -> WayPoint:
        """
        Return GPX first point.
        """
        return self.trk[0].trkseg[0].trkpt[0]

    def last_point(self) -> WayPoint:
        """
        Return GPX last point.
        """
        return self.trk[-1].trkseg[-1].trkpt[-1]

    def extreme_points(self) -> Tuple[WayPoint, WayPoint, WayPoint, WayPoint]:
        """
        Find extreme points in track, i.e.: points with lowest and
        highest latitude and longitude.

        Returns:
            Tuple[WayPoint, WayPoint, WayPoint, WayPoint]: Min latitude
                point, min longitude point, max latitude point, max
                longitude point.
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
        Return the total distance (in meters) of tracks contained in
        the Gpx element.
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
        Return distance from start at each point.
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
        Return the total ascent (in meters) of tracks contained in the
        Gpx element.
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
        Return the total descent (in meters) of tracks contained in the
        Gpx element.
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
        Return minimum elevation (in meters) in tracks contained in the
        Gpx element.
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
        Return maximum elevation (in meters) in tracks contained in the
        Gpx element.
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
                    except ZeroDivisionError:
                        track_point.ascent_rate = 0.0
                    previous_point = track_point

    def min_ascent_rate(self) -> float:
        """
        Return activity minimum ascent rate.
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
        """
        return self.trk[0].trkseg[0].trkpt[0].time

    def utc_stop_time(self):
        """
        Return the activity UTC stop time.
        """
        return self.trk[-1].trkseg[-1].trkpt[-1].time

    def start_time(self) -> datetime:
        """
        Return the activity start time.
        """
        start_time = None
        try:
            start_time = (
                self.trk[0]
                .trkseg[0]
                .trkpt[0]
                .time.replace(tzinfo=timezone.utc)
                .astimezone(tz=None)
            )
        except AttributeError:
            warnings.warn("Unable to find activity start time")
        return start_time

    def stop_time(self) -> datetime:
        """
        Return the activity stop time.
        """
        stop_time = None
        try:
            stop_time = (
                self.trk[-1]
                .trkseg[-1]
                .trkpt[-1]
                .time.replace(tzinfo=timezone.utc)
                .astimezone(tz=None)
            )
        except AttributeError:
            warnings.warn("Unable to find activity stop time")
        return stop_time

    def total_elapsed_time(self) -> datetime:
        """
        Return the total elapsed time.
        """
        total_elapsed_time = None
        try:
            total_elapsed_time = self.stop_time() - self.start_time()
        except TypeError:
            warnings.warn("Unable to compute activity total elapsed time")
        return total_elapsed_time

    def stopped_time(self, tolerance: float = 2.45) -> datetime:
        """
        Return the stopped time during activity.

        Args:
            tolerance (float, optional): Maximal distance between two
                points for movement. Defaults to 2.45.

        Returns:
            datetime: Stopped time.
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
        Return the moving time during the activity.
        """
        return self.total_elapsed_time() - self.stopped_time()

    ###############################################################################
    #### Speed and Pace ###########################################################
    ###############################################################################

    def avg_speed(self) -> float:
        """
        Return the average speed (kilometers per hour) during the activity.
        """
        # Compute and convert total elapsed time
        total_elapsed_time = self.total_elapsed_time()
        total_elapsed_time = total_elapsed_time.total_seconds() / 3600

        # Compute and convert distance
        distance = self.distance() / 1000

        return distance / total_elapsed_time

    def avg_moving_speed(self) -> float:
        """
        Return the average moving speed (kilometers per hour) during the activity.
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

        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    distance = (
                        haversine_distance(previous_point, track_point) / 1000
                    )  # Convert to kilometers
                    # Convert to hours
                    time = (
                        track_point.time - previous_point.time
                    ).total_seconds() / 3600
                    try:
                        track_point.speed = distance / time
                    except ZeroDivisionError:
                        track_point.speed = 0.0
                    previous_point = track_point

    def min_speed(self) -> float:
        """
        Return the minimum speed during the activity.
        """
        self.compute_points_speed()
        min_speed = 1000.0
        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    min_speed = min(min_speed, track_point.speed)
        return min_speed

    def max_speed(self) -> float:
        """
        Return the maximum speed during the activity.
        """
        self.compute_points_speed()
        max_speed = -1.0
        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    max_speed = max(max_speed, track_point.speed)
        return max_speed

    def avg_pace(self) -> float:
        """
        Return the average pace (minute per kilometer) during the activity.
        """
        return 60.0 / self.avg_speed()

    def avg_moving_pace(self) -> float:
        """
        Return the average moving pace (minute per kilometer) during the activity.
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
                    except ZeroDivisionError:
                        # Fill with average moving pace (first point)
                        point.pace = self.avg_moving_pace()

    def min_pace(self) -> float:
        """
        Return the minimum pace during the activity.
        """
        self.compute_points_pace()
        min_pace = 1000.0
        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    min_pace = min(min_pace, track_point.pace)
        return min_pace

    def max_pace(self) -> float:
        """
        Return the maximum pace during the activity.
        """
        self.compute_points_pace()
        max_pace = -1.0
        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    max_pace = max(max_pace, track_point.pace)
        return max_pace

    def compute_points_ascent_speed(self) -> None:
        """
        Compute ascent speed (kilometers per hour) at each track point.
        """
        previous_point = self.first_point()

        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    ascent = (
                        track_point.ele - previous_point.ele
                    ) / 1000  # Convert to kilometers
                    # Convert to hours
                    time = (
                        track_point.time - previous_point.time
                    ).total_seconds() / 3600
                    try:
                        track_point.ascent_speed = ascent / time
                    except ZeroDivisionError:
                        track_point.ascent_speed = 0.0
                    previous_point = track_point

    def min_ascent_speed(self) -> float:
        """
        Return the minimum ascent speed (kilometers per hour) during the activity.
        """
        self.compute_points_ascent_speed()
        min_ascent_speed = 1000.0
        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    min_ascent_speed = min(min_ascent_speed, track_point.ascent_speed)
        return min_ascent_speed

    def max_ascent_speed(self) -> float:
        """
        Return the maximum ascent speed (kilometers per hour) during the activity.
        """
        self.compute_points_ascent_speed()
        max_ascent_speed = -1.0
        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    max_ascent_speed = max(max_ascent_speed, track_point.ascent_speed)
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
        """
        TODO

        Args:
            remove_factor (int, optional): _description_. Defaults to 2.
        """
        count = 0
        for track in self.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if count % remove_factor == 0:
                        track_segment.trkpt.remove(track_point)
                        count += 1

    def remove_gps_errors(self, error_distance: float = 100) -> list:
        """
        Remove GPS errors.

        Args:
            error_distance (float, optional): Error threshold distance
                (in meters) between two points. Defaults to 100.

        Returns:
            list: List of removed points (GPS errors).
        """
        previous_point = None
        gps_errors = []

        for track in self.trk:
            for track_segment in track.trkseg:
                new_trkpt = []

                for track_point in track_segment.trkpt:
                    # GPS error
                    dst = haversine_distance(previous_point, track_point)
                    if previous_point is not None and dst > error_distance:
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
            min_dist (float, optional): Minimal distance (in meters)
                between two points. Defaults to 1.
            max_dist (float, optional): Maximal distance (in meters)
                between two points. Defaults to 10.
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
                        if (
                            haversine_distance(point_1, point_2) < min_dist
                            or haversine_distance(point_2, point) < min_dist
                        ) and haversine_distance(point_1, point) < max_dist:
                            point_2 = point
                        else:
                            new_trkpt.append(point_2)
                            point_1 = point_2
                            point_2 = point

                segment.trkpt = new_trkpt

    ###############################################################################
    #### Simplification ###########################################################
    ###############################################################################

    def simplify(self, epsilon: float):
        """
        Simplify GPX trk using Ramer-Douglas-Peucker algorithm.

        Args:
            epsilon (float): Tolerance.  TODO: add default value
        """
        for track in self.trk:
            for segment in track.trkseg:
                segment.trkpt = ramer_douglas_peucker(segment.trkpt, epsilon)

    ###############################################################################
    #### Exports ##################################################################
    ###############################################################################

    def to_dict(
        self,
        values: list[str] = None,
        as_series: bool = False,
    ) -> dict:
        """
        Convert GPX object to dictionary.
        See: https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.to_dict.html

        Args:
            values (list[str], optional): List of values to write.
                Supported values: "lat", "lon", "ele", "time", "speed",
                "pace", "ascent_rate", "ascent_speed",
                "distance_from_start". Defaults to None.
            as_series (bool, optional): True -> Values are Series,
                False -> Values are list[Any]. Defaults to False.

        Returns:
            dict: Dictionary representing the GPX.
        """
        return self.to_polars(values).to_dict(as_series=as_series)

    def to_dicts(
        self,
        values: list[str] = None,
    ) -> list[dict[str, Any]]:
        """
        Convert GPX object to list of dictionaries.
        See: https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.to_dicts.html

        Args:
            values (list[str], optional): List of values to write.
                Supported values: "lat", "lon", "ele", "time", "speed",
                "pace", "ascent_rate", "ascent_speed",
                "distance_from_start". Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries representing the GPX.
        """
        return self.to_polars(values).to_dicts()

    def _to_dict_df(self, values: list[str] = None) -> dict:
        """
        Convert GPX object to dictionary.

        Args:
            values (list[str], optional): List of values to write.
                Supported values: "lat", "lon", "ele", "time", "speed",
                "pace", "ascent_rate", "ascent_speed",
                "distance_from_start". Defaults to None.

        Returns:
            dict: Dictionary containing data from GPX.
        """
        # Set default parameter
        if values is None:
            values = ["lat", "lon"]

        # Compute required values
        test_point = self.first_point()
        if "speed" in values and test_point.speed is None:
            self.compute_points_speed()
        if "pace" in values and test_point.pace is None:
            self.compute_points_pace()
        if "ascent_rate" in values and test_point.ascent_rate is None:
            self.compute_points_ascent_rate()
        if "ascent_speed" in values and test_point.ascent_speed is None:
            self.compute_points_ascent_speed()
        if "distance_from_start" in values and test_point.distance_from_start is None:
            self.compute_points_distance_from_start()

        # Create dataframe
        gpx_data = {}
        for v in values:
            if v == "time":
                gpx_data[v] = [
                    str(trkpt.time.replace(tzinfo=timezone.utc).astimezone(tz=None))
                    for trk in self.trk
                    for trkseg in trk.trkseg
                    for trkpt in trkseg.trkpt
                ]
            else:
                gpx_data[v] = [
                    getattr(trkpt, v)
                    for trk in self.trk
                    for trkseg in trk.trkseg
                    for trkpt in trkseg.trkpt
                ]
        return gpx_data

    def to_pandas(self, values: list[str] = None) -> pd.DataFrame:
        """
        Convert GPX object to Pandas Dataframe.
        Missing values are filled with default values (0 for numerical
        values and empty string for text).

        Args:
            values (list[str], optional): List of values to write.
                Supported values: "lat", "lon", "ele", "time", "speed",
                "pace", "ascent_rate", "ascent_speed",
                "distance_from_start". Defaults to None.

        Returns:
            pd.DataFrame: Dataframe containing data from GPX.
        """
        return pd.DataFrame(self._to_dict_df(values))

    def to_polars(self, values: list[str] = None) -> pl.DataFrame:
        """
        Convert GPX object to Polars Dataframe.
        Missing values are filled with default values (0 for numerical
        values and empty string for text).

        Args:
            values (list[str], optional): List of values to write.
                Supported values: "lat", "lon", "ele", "time", "speed",
                "pace", "ascent_rate", "ascent_speed",
                "distance_from_start". Defaults to None.

        Returns:
            pl.DataFrame: Dataframe containing data from GPX.
        """
        return pl.DataFrame(self._to_dict_df(values))

    def to_csv(
        self,
        dest: Optional[str | Path | IO[str] | IO[bytes] | bytes] = None,
        values: list[str] = None,
        **kwargs,
    ) -> str | None:
        """
        Write the GPX object track coordinates to a CSV file.

        Args:
            dest (str | Path | IO[str] | IO[bytes] | bytes, optional):
                Path to a file or a file-like object to write in.
                Defaults to None.
            values (list[str], optional): list of values to write.
                Supported values: "lat", "lon", "ele", "time", "speed",
                "pace", "ascent_rate", "ascent_speed",
                "distance_from_start". Defaults to None.

        Returns:
            str | None: CSV like string if path is set to None.
        """
        if values is None:
            values = ["lat", "lon"]

        if isinstance(dest, bytes):
            dest = io.BytesIO(dest)

        # Argument columns is required for KML writer (keep values order)
        return self.to_polars(values).select(values).write_csv(dest, **kwargs)
