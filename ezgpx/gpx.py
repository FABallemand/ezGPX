"""
This file contains the high level GPX object.
"""

from __future__ import annotations

import io
import warnings
from datetime import datetime, timezone
from math import degrees
from pathlib import Path
from typing import IO, Any, Optional
from zipfile import ZipFile

import narwhals as nw
import pandas as pd
import polars as pl
from narwhals.typing import IntoFrameT

from .complex_types import (
    Bounds,
    Copyright,
    Email,
    Extensions,
    Gpx,
    Link,
    Metadata,
    Person,
    Pt,
    Ptseg,
    Rte,
    Trk,
    Trkseg,
    Wpt,
)
from .constants.precisions import DEFAULT_PRECISION_DICT, DEFAULT_TIME_FORMAT
from .parsers.fit_parser import FitParser
from .parsers.gpx_parser import GPXParser
from .parsers.kml_parser import KMLParser
from .utils import (
    EARTH_RADIUS,
    check_xml_extensions_schemas,
    check_xml_schema,
    haversine_distance,
    ramer_douglas_peucker,
)
from .utils.dataframe import is_dataframe
from .writers.gpx_writer import GPXWriter
from .writers.kml_writer import KMLWriter


class GPX:
    """
    High level GPX object.
    """

    TIME_RELATED_VALUES = ["time", "speed", "pace", "ascent_speed"]
    ELEVATION_RELATED_VALUES = ["ele", "ascent_rate", "ascent_speed"]

    def __init__(
        self,
        source: Optional[str | Path | IO[str] | IO[bytes] | bytes | IntoFrameT] = None,
        xml_schema: bool = True,
        xml_extensions_schemas: bool = False,
    ) -> None:
        """
        Initialise high level GPX object.

        Args:
            source (str | Path | IO[str] | IO[bytes] | bytes | IntoFrameT, optional):
                Path to a file or a file-like object to parse. Defaults to None.
            xml_schemas (bool, optional): Toggle schema
                verification during parsing. Defaults to True.
            xml_extensions_schemas (bool, optional): Toggle extensions
                schema verificaton durign parsing. Requires internet connection
                connection and is not guaranted to work. Defaults to False.
        Raises:
            FileNotFoundError: _description_
            ValueError: _description_
            FileNotFoundError: _description_
        """
        # GPX file description
        self.source: str | Path | IO[str] | IO[bytes] | bytes | IntoFrameT = None

        # GPX file content
        self.gpx: Gpx = None
        self._ele_data: bool = False
        self._time_data: bool = False
        self._precisions: dict = DEFAULT_PRECISION_DICT
        self._time_format: str = DEFAULT_TIME_FORMAT
        self._extensions_fields: dict = {}

        # Writers
        self._gpx_writer: GPXWriter = None
        self._kml_writer: KMLWriter = None

        # Markers
        self._dist_from_start = False
        self.ascent_rate = False
        self._speed: bool = False
        self._pace: bool = False
        self._ascent_speed: bool = False

        # Empty source - Create empty GPX instance for advanced use only
        if source is None:
            self._init_from_none()
        # Valid file
        elif isinstance(source, (str, Path)):
            self.source = Path(source)

            # GPX
            if self.source.suffix == ".gpx":
                self._init_from_gpx(xml_schema, xml_extensions_schemas)

            # KML
            elif self.source.suffix == ".kml":
                self._init_from_kml()

            # KMZ
            elif self.source.suffix == ".kmz":
                self._init_from_kmz(xml_schema, xml_extensions_schemas)

            # FIT
            elif self.source.suffix == ".fit":
                self._init_from_fit()

            # Invalid file or file path
            else:
                raise ValueError(
                    f"Unable to parse this type of file: {source}"
                    "Consider renaming your file with the proper file extension."
                )

            # Writers
            self._gpx_writer = GPXWriter(self.gpx, self._precisions, self._time_format)
            self._kml_writer = KMLWriter(
                self.gpx, precisions=self._precisions, time_format=self._time_format
            )

        # Dataframe
        elif is_dataframe(source):
            self._init_from_dataframe(source)
        else:
            raise TypeError(
                f"Invalid source type: {type(source)}. "
                "Expected str, Path, IO[str], IO[bytes], bytes, pd.DataFrame or pl.DataFrame."
            )

    def _init_from_none(self):
        """
        Initialise empty GPX instance.
        """
        warnings.warn(
            "No file path provided, creating an empty GPX instance.", UserWarning
        )
        self.gpx = Gpx("1.1", "ezGPX")

        # Writers
        self._gpx_writer = GPXWriter(self.gpx)
        self._kml_writer = KMLWriter(self.gpx)

    def _init_from_gpx(
        self, xml_schema: bool = True, xml_extensions_schemas: bool = False
    ):
        """
        Initialise GPX instance from GPX file.

        Args:
            xml_schemas (bool, optional): Toggle schema
                verification during parsing. Defaults to True.
            xml_extensions_schemas (bool, optional): Toggle extensions
                schema verificaton durign parsing. Requires internet connection
                connection and is not guaranted to work. Defaults to False.
        """
        parser = GPXParser(self.source, xml_schema, xml_extensions_schemas)
        self.gpx = parser.gpx
        self._ele_data = parser.ele_data
        self._time_data = parser.time_data
        self._precisions = parser.precisions
        self._time_format = parser.time_format
        self._extensions_fields = parser.extensions_fields

    def _init_from_kml(
        self, xml_schema: bool = True, xml_extensions_schemas: bool = False
    ):
        """
        Initialise GPX instance from KML file.

        Args:
            xml_schemas (bool, optional): Toggle schema
                verification during parsing. Defaults to True.
            xml_extensions_schemas (bool, optional): Toggle extensions
                schema verificaton durign parsing. Requires internet connection
                connection and is not guaranted to work. Defaults to False.
        """
        parser = KMLParser(self.source, xml_schema, xml_extensions_schemas)
        self.gpx = parser.gpx
        self._precisions = parser.precisions
        self._time_format = parser.time_format

    def _init_from_kmz(
        self, xml_schema: bool = True, xml_extensions_schemas: bool = False
    ):
        """
        Initialise GPX instance from KMZ file.

        Args:
            xml_schemas (bool, optional): Toggle schema
                verification during parsing. Defaults to True.
            xml_extensions_schemas (bool, optional): Toggle extensions
                schema verificaton durign parsing. Requires internet connection
                connection and is not guaranted to work. Defaults to False.
        """
        with ZipFile(self.source, "r") as kmz:
            kmls = [
                info.filename
                for info in kmz.infolist()
                if info.filename.endswith(".kml")
            ]
            if "doc.kml" not in kmls:
                raise FileNotFoundError(
                    f"Unable to parse file: {self.source}"
                    "Expected to find doc.kml inside KMZ file."
                )
            with kmz.open("doc.kml", "r") as kml_file:
                kml = io.BytesIO(kml_file.read())
        parser = KMLParser(kml, xml_schema, xml_extensions_schemas)
        self.gpx = parser.gpx
        self._precisions = parser.precisions
        self._time_format = parser.time_format

    def _init_from_fit(self):
        """
        Initialise GPX instance from FIT file.
        """
        parser = FitParser(self.source)
        self.gpx = parser.gpx
        self._precisions = parser.precisions
        self._time_format = parser.time_format

    def _init_from_dataframe(self, source: IntoFrameT):
        """
        Initialize Gpx from dataframe.

        Args:
            df (IntoFrameT): Dataframe with "lat", "lon" columns. Also
                supports "ele", "time" columns.
        """
        df = nw.from_native(source)

        trkpt = [
            Wpt(
                tag="trkpt",
                lat=row["lat"],
                lon=row["lon"],
                ele=row.get("ele"),
                time=row.get("time"),
            )
            for row in df.iter_rows(named=True)
        ]
        trkseg = Trkseg(trkpt=trkpt)
        trk = Trk(trkseg=[trkseg])
        return Gpx("1.1", "ezGPX", trk=[trk])

    def __str__(self) -> str:
        return self._gpx_writer.gpx_to_string()

    def __repr__(self):
        return f"source = {self.source}\ngpx = {self.gpx}"

    ###############################################################################
    #### Schemas ##################################################################
    ###############################################################################

    def check_xml_schema(self) -> bool:
        """
        Check XML schema.

        Returns:
            bool: True if the file follows XML schemas.
        """
        return check_xml_schema(self.source, self.gpx.version)

    def check_xml_extensions_schemas(self) -> bool:
        """
        Check XML extension schemas.

        Returns:
            bool: True if the file follows XML schemas.
        """
        return check_xml_extensions_schemas(self.source)

    ###############################################################################
    #### Name #####################################################################
    ###############################################################################

    def name(self) -> str:
        """
        Return activity name.
        """
        return self.gpx.metadata.name

    def set_name(self, new_name: str) -> None:
        """
        Set activity name.

        Args:
            new_name (str): New activity name.
        """
        self.gpx.metadata.name = new_name

    ###############################################################################
    #### Points ###################################################################
    ###############################################################################

    def nb_points(self) -> int:
        """
        Return the number of points in the GPX.
        """
        nb_pts = 0
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                nb_pts += len(track_segment.trkpt)
        return nb_pts

    def bounds(self) -> tuple[float, float, float, float]:
        """
        Return minimum and maximum latitude and longitude.

        Returns:
            Tuple[float, float, float, float]: Min latitude, min
                longitude, max latitude, max longitude.
        """
        min_lat = self.gpx.trk[0].trkseg[0].trkpt[0].lat
        min_lon = self.gpx.trk[0].trkseg[0].trkpt[0].lon
        max_lat = min_lat
        max_lon = min_lon

        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    min_lat = min(min_lat, track_point.lat)
                    min_lon = min(min_lon, track_point.lon)
                    max_lat = max(max_lat, track_point.lat)
                    max_lon = max(max_lon, track_point.lon)
        return min_lat, min_lon, max_lat, max_lon

    def center(self) -> tuple[float, float]:
        """
        Return latitude and longitude of the center point.
        """
        min_lat, min_lon, max_lat, max_lon = self.bounds()
        center_lat = min_lat + (max_lat - min_lat) / 2
        center_lon = min_lon + (max_lon - min_lon) / 2
        return center_lat, center_lon

    def get_trkpt(self, trk_index: int, trkseg_index: int, trkpt_index: int) -> Wpt:
        """
        Return track point based on track, track segment and track
        point indexes.

        Args:
            trk_index (int): Track index.
            trkseg_index (int): Track segment index.
            trkpt_index (int): Track point index.

        Returns:
            Wpt: Track point.
        """
        return self.gpx.trk[trk_index].trkseg[trkseg_index].trkpt[trkpt_index]

    def extreme_points(
        self,
    ) -> tuple[Wpt, Wpt, Wpt, Wpt]:
        """
        Return extreme points in track, i.e.: points with lowest and
        highest latitude and longitude.

        Returns:
            tuple[Wpt, Wpt, Wpt, Wpt]: Min latitude
                point, min longitude point, max latitude point, max
                longitude points.
        """
        min_lat_point = self.gpx.trk[0].trkseg[0].trkpt[0]
        min_lon_point = self.gpx.trk[0].trkseg[0].trkpt[0]
        max_lat_point = self.gpx.trk[0].trkseg[0].trkpt[0]
        max_lon_point = self.gpx.trk[0].trkseg[0].trkpt[0]

        for track in self.gpx.trk:
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
        Return the total distance of tracks (in meters).
        """
        dst = 0.0
        previous_point = self.gpx.trk[0].trkseg[0].trkpt[0]
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    dst += haversine_distance(previous_point, track_point)
                    previous_point = track_point
        return dst

    def _compute_distance_from_start(self):
        """
        Return distance from start at each point.
        """
        if self._dist_from_start:
            return
        dst = 0.0
        previous_point = self.gpx.trk[0].trkseg[0].trkpt[0]
        previous_point.distance_from_start = dst
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    dst += haversine_distance(previous_point, track_point)
                    track_point.distance_from_start = dst
                    previous_point = track_point
        self._dist_from_start = True

    def ascent(self) -> float:
        """
        Return the total ascent of tracks (in meters).
        """
        ascent = 0
        previous_elevation = self.gpx.trk[0].trkseg[0].trkpt[0].ele
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ele > previous_elevation:
                        ascent += track_point.ele - previous_elevation
                    previous_elevation = track_point.ele
        return ascent

    def descent(self) -> float:
        """
        Return the total descent of tracks (in meters).
        """
        descent = 0
        previous_elevation = self.gpx.trk[0].trkseg[0].trkpt[0].ele
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    if track_point.ele < previous_elevation:
                        descent += previous_elevation - track_point.ele
                    previous_elevation = track_point.ele
        return descent

    def min_elevation(self) -> float:
        """
        Returns the minimum elevation (in meters).
        """
        min_elevation = self.gpx.trk[0].trkseg[0].trkpt[0].ele
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    min_elevation = min(min_elevation, track_point.ele)
        return min_elevation

    def max_elevation(self) -> float:
        """
        Returns the maximum elevation (in meters).
        """
        max_elevation = self.gpx.trk[0].trkseg[0].trkpt[0].ele
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    max_elevation = max(max_elevation, track_point.ele)
        return max_elevation

    def _compute_ascent_rate(self) -> None:
        """
        Compute ascent rate at each point.
        """
        if self.ascent_rate:
            return
        previous_point = self.gpx.trk[0].trkseg[0].trkpt[0]
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    distance = haversine_distance(previous_point, track_point)
                    ascent = track_point.ele - previous_point.ele
                    try:
                        track_point.ascent_rate = (ascent * 100) / distance
                    except ZeroDivisionError:
                        track_point.ascent_rate = 0.0
                    previous_point = track_point
        self.ascent_rate = True

    def max_descent_rate(self) -> float:
        """
        Return the minimum ascent rate.
        """
        self._compute_ascent_rate()
        min_ascent_rate = 100.0
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    min_ascent_rate = min(min_ascent_rate, track_point.ascent_rate)
        return min_ascent_rate

    def max_ascent_rate(self) -> float:
        """
        Return the maximum ascent rate.
        """
        self._compute_ascent_rate()
        max_ascent_rate = -1.0
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    max_ascent_rate = max(max_ascent_rate, track_point.ascent_rate)
        return max_ascent_rate

    ###############################################################################
    #### Time #####################################################################
    ###############################################################################

    def start_time(self) -> datetime:
        """
        Return the UTC start time.
        """
        return self.gpx.trk[0].trkseg[0].trkpt[0].time

    def stop_time(self) -> datetime:
        """
        Return the UTC stop time.
        """
        return self.gpx.trk[-1].trkseg[-1].trkpt[-1].time

    # TODO
    # def start_time(self) -> datetime:
    #     """
    #     Return the activity start time.
    #     """
    #     start_time = None
    #     try:
    #         start_time = (
    #             self.trk[0]
    #             .trkseg[0]
    #             .trkpt[0]
    #             .time.replace(tzinfo=timezone.utc)
    #             .astimezone(tz=None)
    #         )
    #     except AttributeError:
    #         warnings.warn("Unable to find activity start time")
    #     return start_time

    # TODO
    # def stop_time(self) -> datetime:
    #     """
    #     Return the activity stop time.
    #     """
    #     stop_time = None
    #     try:
    #         stop_time = (
    #             self.trk[-1]
    #             .trkseg[-1]
    #             .trkpt[-1]
    #             .time.replace(tzinfo=timezone.utc)
    #             .astimezone(tz=None)
    #         )
    #     except AttributeError:
    #         warnings.warn("Unable to find activity stop time")
    #     return stop_time

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
        Return the stopped time.

        Args:
            tolerance (float, optional): Maximal distance between two
                points for movement. Defaults to 2.45.

        Returns:
            datetime: Stopped time.
        """
        stopped_time = (
            self.start_time() - self.start_time()
        )  # TODO Better way to do it?
        previous_point = self.gpx.trk[0].trkseg[0].trkpt[0]
        for track in self.gpx.trk:
            for segment in track.trkseg:
                for point in segment.trkpt:
                    if haversine_distance(previous_point, point) < tolerance:
                        stopped_time += point.time - previous_point.time
                    previous_point = point
        return stopped_time

    def moving_time(self) -> datetime:
        """
        Return the moving time.
        """
        return self.total_elapsed_time() - self.stopped_time()

    ###############################################################################
    #### Speed and Pace ###########################################################
    ###############################################################################

    def _compute_speed(self) -> None:
        """
        Compute speed (in kilometers per hour) at each track point.
        """
        if self._speed:
            return
        previous_point = self.gpx.trk[0].trkseg[0].trkpt[0]
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    distance = (
                        haversine_distance(previous_point, track_point) / 1000
                    )  # Distance in kilometers
                    time = (
                        track_point.time - previous_point.time
                    ).total_seconds() / 3600  # Time in hours
                    try:
                        track_point.speed = distance / time
                    except ZeroDivisionError:
                        track_point.speed = 0.0
                    previous_point = track_point
        self._speed = True

    def avg_speed(self, moving: bool = False) -> float:
        """
        Return the average speed (in kilometers per hour).

        Args:
            moving (bool, optional): Moving flag. Defaults to False.

        Returns:
            float: Average moving speed if `moving` is True, average
                speed otherwise.
        """
        distance = self.distance() / 1000  # Distance in kilometers
        if moving:
            time = self.moving_time().total_seconds() / 3600  # Moving time in hours
        else:
            time = (
                self.total_elapsed_time().total_seconds() / 3600
            )  # Total elapsed time in hours
        return distance / time

    def min_speed(self) -> float:
        """
        Return the minimum speed (in kilometers per hour).
        """
        self._compute_speed()
        min_speed = 1_000.0
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    min_speed = min(min_speed, track_point.speed)
        return min_speed

    def max_speed(self) -> float:
        """
        Return the maximum speed (in kilometers per hour).
        """
        self._compute_speed()
        max_speed = -1.0
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    max_speed = max(max_speed, track_point.speed)
        return max_speed

    def _compute_pace(self) -> None:
        """
        Compute pace (in minutes per kilometer) at each track point.
        """
        if self._pace:
            return
        self._compute_speed()
        for track in self.gpx.trk:
            for segment in track.trkseg:
                for point in segment.trkpt:
                    try:
                        point.pace = 60.0 / point.speed
                    except ZeroDivisionError:
                        point.pace = 0.0
        self._pace = True

    def avg_pace(self, moving: bool = False) -> float:
        """
        Return the average pace (in minutes per kilometer).

        Args:
            moving (bool, optional): Moving flag. Defaults to False.

        Returns:
            float: Average moving pace if `moving` is True, average
                pace otherwise.
        """
        return 60.0 / self.avg_speed(moving)

    def min_pace(self) -> float:
        """
        Return the minimum pace (in minutes per kilometer).
        """
        self._compute_pace()
        min_pace = 1000.0
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    min_pace = min(min_pace, track_point.pace)
        return min_pace

    def max_pace(self) -> float:
        """
        Return the maximum pace (in minutes per kilometer).
        """
        self._compute_pace()
        max_pace = -1.0
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    max_pace = max(max_pace, track_point.pace)
        return max_pace

    def _compute_ascent_speed(self) -> None:
        """
        Compute ascent speed (in kilometers per hour) at each track point.
        """
        if self._ascent_speed:
            return
        previous_point = self.gpx.trk[0].trkseg[0].trkpt[0]
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    ascent = track_point.ele - previous_point.ele
                    # Convert to hours
                    time = (
                        track_point.time - previous_point.time
                    ).total_seconds() / 3600
                    try:
                        track_point.ascent_speed = ascent / time
                    except ZeroDivisionError:
                        track_point.ascent_speed = 0.0
                    previous_point = track_point
        self._ascent_speed = True

    def min_ascent_speed(self) -> float:
        """
        Return the minimum ascent speed (in meters per hour).
        """
        self._compute_ascent_speed()
        min_ascent_speed = 1000.0
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    min_ascent_speed = min(min_ascent_speed, track_point.ascent_speed)
        return min_ascent_speed

    def max_ascent_speed(self) -> float:
        """
        Return the maximum ascent speed (in meters per hour).
        """
        self._compute_ascent_speed()
        max_ascent_speed = -1.0
        for track in self.gpx.trk:
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
        self.gpx.metadata = None

    def remove_elevation(self):
        """
        Remove elevation data.
        """
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    track_point.ele = None

    def remove_time(self):
        """
        Remove time data.
        """
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                for track_point in track_segment.trkpt:
                    track_point.time = None

    def remove_extensions(self):
        """
        Remove extensions data.
        """
        self.gpx.extensions = None  # Remove extensions from gpx
        self.gpx.metadata.extensions = None  # Remove extensions from metadata
        # Remove extensions from waypoints
        if self.gpx.wpt is not None:
            for pt in self.gpx.wpt:
                pt.extensions = None
        # Remove extensions from routes
        if self.gpx.rte is not None:
            for rt in self.gpx.rte:
                rt.extensions = None
        # Remove extensions from tracks, track segments and track points
        if self.gpx.trk is not None:
            for track in self.gpx.trk:
                track.extensions = None
                if track.trkseg is not None:
                    for track_segment in track.trkseg:
                        track_segment.extensions = None
                        if track_segment.trkpt is not None:
                            for track_point in track_segment.trkpt:
                                track_point.extensions = None

    ###############################################################################
    #### Error Correction #########################################################
    ###############################################################################

    # TODO
    # def remove_points(self, remove_factor: int = 2):
    #     """
    #     TODO

    #     Args:
    #         remove_factor (int, optional): _description_. Defaults to 2.
    #     """
    #     count = 0
    #     for track in self.trk:
    #         for track_segment in track.trkseg:
    #             for track_point in track_segment.trkpt:
    #                 if count % remove_factor == 0:
    #                     track_segment.trkpt.remove(track_point)
    #                     count += 1

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
        for track in self.gpx.trk:
            for track_segment in track.trkseg:
                new_trkpt = []
                for track_point in track_segment.trkpt:
                    # GPS error
                    dst = haversine_distance(previous_point, track_point)
                    if (
                        previous_point is not None and dst > error_distance
                    ):  # TODO use Z-score?
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
            min_dist (float, optional): Minimal distance between two
                points. Defaults to 1.
            max_dist (float, optional): Maximal distance between two
                points. Defaults to 10.
        """
        point_1 = None
        point_2 = None
        for track in self.gpx.trk:
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

    def simplify(self, tolerance: float = 2):
        """
        Simplify tracks using Ramer-Douglas-Peucker algorithm.

        Args:
            tolerance (float, optional): Minimum distance (in meters)
            between the point and the track before the point is
            removed. Defaults to 2.
        """
        epsilon = degrees(tolerance / EARTH_RADIUS)
        for track in self.gpx.trk:
            for segment in track.trkseg:
                segment.trkpt = ramer_douglas_peucker(segment.trkpt, epsilon)

    ###############################################################################
    #### Merge ####################################################################
    ###############################################################################

    @staticmethod
    def merge(gpx_1: GPX, gpx_2: GPX) -> GPX:
        """
        Merge GPX objects into a new instance.

        Args:
            gpx_1 (GPX): First GPX object.
            gpx_2 (GPX): Second GPX object.

        Returns:
            GPX: Merged GPX (new instance).
        """
        topo = [
            "http://www.topografix.com/GPX/1/1",
            "http://www.topografix.com/GPX/1/1/gpx.xsd",
        ]

        # Create new GPX instance
        merged_gpx = GPX()

        # Fill new GPX instance
        merged_gpx.gpx.tag = "gpx"
        merged_gpx.gpx.xmlns = "http://www.topografix.com/GPX/1/1"
        merged_gpx.gpx.xsi_schema_location = list(
            set(topo + gpx_1.gpx.xsi_schema_location + gpx_2.gpx.xsi_schema_location)
        )
        merged_gpx.gpx.version = "1.1"
        merged_gpx.gpx.creator = "ezGPX"
        merged_gpx.gpx.metadata = (
            gpx_2.gpx.metadata if gpx_1.gpx.metadata is None else gpx_1.gpx.metadata
        )
        merged_gpx.gpx.wpt = gpx_1.gpx.wpt + gpx_2.gpx.wpt
        merged_gpx.gpx.rte = gpx_1.gpx.rte + gpx_2.gpx.rte
        merged_gpx.gpx.trk = gpx_1.gpx.trk + gpx_2.gpx.trk
        merged_gpx.gpx.extensions = Extensions(
            "extensions", gpx_1.gpx.metadata | gpx_2.gpx.metadata
        )

        # Return new GPX instance
        return merged_gpx

    ###############################################################################
    #### Exports ##################################################################
    ###############################################################################

    def to_dict(
        self,
        values: list[str] = None,
        as_series: bool = False,
    ) -> dict:
        """
        Convert GPX object to dictionary (similar to Polars
        `to_dict`).

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
        Convert GPX object to list of dictionaries (similar to Polars
        `to_dicts`).

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
        test_point = self.gpx.trk[0].trkseg[0].trkpt[0]
        if "speed" in values and test_point.speed is None:
            self._compute_speed()
        if "pace" in values and test_point.pace is None:
            self._compute_pace()
        if "ascent_rate" in values and test_point.ascent_rate is None:
            self._compute_ascent_rate()
        if "ascent_speed" in values and test_point.ascent_speed is None:
            self._compute_ascent_speed()
        if "distance_from_start" in values and test_point.distance_from_start is None:
            self._compute_distance_from_start()

        # Create dataframe
        gpx_data = {}
        for v in values:
            if v == "time":
                gpx_data[v] = [
                    str(trkpt.time.replace(tzinfo=timezone.utc).astimezone(tz=None))
                    for trk in self.gpx.trk
                    for trkseg in trk.trkseg
                    for trkpt in trkseg.trkpt
                ]
            else:
                gpx_data[v] = [
                    getattr(trkpt, v)
                    for trk in self.gpx.trk
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
        # Set default parameter
        if values is None:
            values = ["lat", "lon"]

        # Disable time related values if no time data available
        if not self._time_data:
            if any(v in GPX.TIME_RELATED_VALUES for v in values):
                warnings.warn(
                    f"""Trying to create dataframe from GPX file {self.source}
                        which does not contain time data. Time related values
                        (time, speed, pace, ascent speed) will not be present in
                        the dataframe.""",
                    UserWarning,
                )
            for v in GPX.TIME_RELATED_VALUES:
                if v in values:
                    values.remove(v)

        # Disable elevation related values if no elevation data available
        if not self._ele_data:
            if any(v in GPX.ELEVATION_RELATED_VALUES for v in values):
                warnings.warn(
                    f"""Trying to create dataframe from GPX file {self.source}
                        which does not contain elevation data. Time related
                        values (elevation, ascent rate, ascent speed) will not
                        be present in the dataframe.""",
                    UserWarning,
                )
            for v in GPX.ELEVATION_RELATED_VALUES:
                if v in values:
                    values.remove(v)

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
        # Set default parameter
        if values is None:
            values = ["lat", "lon"]

        # Disable time related values if no time data available
        if not self._time_data:
            if any(v in GPX.TIME_RELATED_VALUES for v in values):
                warnings.warn(
                    f"""Trying to create dataframe from GPX file {self.source}
                        which does not contain time data. Time related values
                        (time, speed, pace, ascent speed) will not be present in
                        the dataframe.""",
                    UserWarning,
                )
            for v in GPX.TIME_RELATED_VALUES:
                if v in values:
                    values.remove(v)

        # Disable elevation related values if no elevation data available
        if not self._ele_data:
            if any(v in GPX.ELEVATION_RELATED_VALUES for v in values):
                warnings.warn(
                    f"""Trying to create dataframe from GPX file {self.source}
                        which does not contain elevation data. Time related
                        values (elevation, ascent rate, ascent speed) will not
                        be present in the dataframe.""",
                    UserWarning,
                )
            for v in GPX.ELEVATION_RELATED_VALUES:
                if v in values:
                    values.remove(v)

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

    def to_gpx(
        self,
        dest: Optional[str | Path | IO[str] | IO[bytes] | bytes] = None,
        *,
        properties: bool = True,
        bounds_fields: Optional[list[str]] = None,
        copyright_fields: Optional[list[str]] = None,
        email_fields: Optional[list[str]] = None,
        extensions_fields: Optional[dict] = None,
        gpx_fields: Optional[list[str]] = None,
        link_fields: Optional[list[str]] = None,
        metadata_fields: Optional[list[str]] = None,
        person_fields: Optional[list[str]] = None,
        point_segment_fields: Optional[list[str]] = None,
        point_fields: Optional[list[str]] = None,
        route_fields: Optional[list[str]] = None,
        track_segment_fields: Optional[list[str]] = None,
        track_fields: Optional[list[str]] = None,
        waypoint_fields: Optional[list[str]] = None,
        track_point_fields: Optional[list[str]] = None,
        mandatory_fields: bool = True,
    ) -> str | None:
        """
        Write the GPX object to a GPX file.

        Args:
            dest (str | Path | IO[str] | IO[bytes] | bytes, optional):
                Path to a file or a file-like object to write in.
                Defaults to None.
            properties (bool, optional): _description_. Defaults to True.
            bounds_fields (Optional[list[str]], optional): _description_. Defaults to None.
            copyright_fields (Optional[list[str]], optional): _description_. Defaults to None.
            email_fields (Optional[list[str]], optional): _description_. Defaults to None.
            extensions_fields (Optional[dict], optional): _description_. Defaults to None.
            gpx_fields (Optional[list[str]], optional): _description_. Defaults to None.
            link_fields (Optional[list[str]], optional): _description_. Defaults to None.
            metadata_fields (Optional[list[str]], optional): _description_. Defaults to None.
            person_fields (Optional[list[str]], optional): _description_. Defaults to None.
            point_segment_fields (Optional[list[str]], optional): _description_. Defaults to None.
            point_fields (Optional[list[str]], optional): _description_. Defaults to None.
            route_fields (Optional[list[str]], optional): _description_. Defaults to None.
            track_segment_fields (Optional[list[str]], optional): _description_. Defaults to None.
            track_fields (Optional[list[str]], optional): _description_. Defaults to None.
            waypoint_fields (Optional[list[str]], optional): _description_. Defaults to None.
            track_point_fields (Optional[list[str]], optional): _description_. Defaults to None.
            mandatory_fields (bool, optional): _description_. Defaults to True.

        Returns:
            str | None: GPX like string if path is set to None.
        """
        bounds_fields = bounds_fields if bounds_fields is not None else Bounds._fields
        copyright_fields = (
            copyright_fields if copyright_fields is not None else Copyright._fields
        )
        email_fields = email_fields if email_fields is not None else Email._fields
        extensions_fields = (
            extensions_fields
            if extensions_fields is not None
            else self._extensions_fields
        )
        gpx_fields = gpx_fields if gpx_fields is not None else Gpx._fields
        link_fields = link_fields if link_fields is not None else Link._fields
        metadata_fields = (
            metadata_fields if metadata_fields is not None else Metadata._fields
        )
        person_fields = person_fields if person_fields is not None else Person._fields
        point_segment_fields = (
            point_segment_fields if point_segment_fields is not None else Ptseg._fields
        )
        point_fields = point_fields if point_fields is not None else Pt._fields
        route_fields = route_fields if route_fields is not None else Rte._fields
        track_segment_fields = (
            track_segment_fields if track_segment_fields is not None else Trkseg._fields
        )
        track_fields = track_fields if track_fields is not None else Trk._fields
        waypoint_fields = (
            waypoint_fields if waypoint_fields is not None else Wpt._fields
        )
        track_point_fields = (
            track_point_fields if track_point_fields is not None else Wpt._fields
        )
        return self._gpx_writer.write(
            file_path=dest,
            properties=properties,
            bounds_fields=bounds_fields,
            copyright_fields=copyright_fields,
            email_fields=email_fields,
            extensions_fields=extensions_fields,
            gpx_fields=gpx_fields,
            link_fields=link_fields,
            metadata_fields=metadata_fields,
            person_fields=person_fields,
            point_segment_fields=point_segment_fields,
            point_fields=point_fields,
            route_fields=route_fields,
            track_segment_fields=track_segment_fields,
            track_fields=track_fields,
            waypoint_fields=waypoint_fields,
            track_point_fields=track_point_fields,
            mandatory_fields=mandatory_fields,
        )

    def to_kml(
        self,
        dest: Optional[str | Path | IO[str] | IO[bytes] | bytes] = None,
        *,
        styles: Optional[list[tuple[str, dict]]] = None,
    ) -> str | None:
        """pt
        Write the GPX object to a KML file.

        Args:
            dest (str | Path | IO[str] | IO[bytes] | bytes, optional):
                Path to a file or a file-like object to write in.
                Defaults to None.
            styles (Optional[list[tuple[str, dict]]], optional): KML
                styles. Defaults to None.

        Returns:
            str | None: KML like string if path is set to None.
        """
        return self._kml_writer.write(dest, styles)
