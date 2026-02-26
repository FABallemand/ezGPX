"""
This file contains the high level GPX object.
"""

from __future__ import annotations

import io
import warnings
from datetime import datetime
from math import degrees
from pathlib import Path
from typing import IO, Dict, List, Optional, Tuple, Union
from zipfile import ZipFile

import pandas as pd
import polars as pl
from narwhals.typing import IntoFrameT

from ..constants.precisions import DEFAULT_PRECISION_DICT, DEFAULT_TIME_FORMAT
from ..gpx_elements import (
    Bounds,
    Copyright,
    Email,
    Extensions,
    Gpx,
    Link,
    Metadata,
    Person,
    Point,
    PointSegment,
    Route,
    Track,
    TrackSegment,
    WayPoint,
)
from ..parsers.fit_parser import FitParser
from ..parsers.gpx_parser import GPXParser
from ..parsers.kml_parser import KMLParser
from ..utils import EARTH_RADIUS, check_xml_extensions_schemas, check_xml_schema
from ..writers.gpx_writer import GPXWriter
from ..writers.kml_writer import KMLWriter


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
        self._precisions: Dict = DEFAULT_PRECISION_DICT
        self._time_format: str = DEFAULT_TIME_FORMAT

        # Parsers
        self._gpx_parser: GPXParser = None  # TODO remove?

        # Writers
        self._gpx_writer: GPXWriter = None
        self._kml_writer: KMLWriter = None

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
        elif isinstance(
            source, (pd.DataFrame, pl.DataFrame)
        ):  # TODO other dataframe types
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
        self.gpx = Gpx()

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
        self._gpx_parser = GPXParser(self.source, xml_schema, xml_extensions_schemas)
        self.gpx = self._gpx_parser.gpx
        self._ele_data = self._gpx_parser.ele_data
        self._time_data = self._gpx_parser.time_data
        self._precisions = self._gpx_parser.precisions
        self._time_format = self._gpx_parser.time_format

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
        kml_parser = KMLParser(self.source, xml_schema, xml_extensions_schemas)
        self.gpx = kml_parser.gpx
        self._precisions = kml_parser.precisions
        self._time_format = kml_parser.time_format

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
            kml = io.BytesIO(kmz.open("doc.kml", "r").read())
        kml_parser = KMLParser(kml, xml_schema, xml_extensions_schemas)
        self.gpx = kml_parser.gpx
        self._precisions = kml_parser.precisions
        self._time_format = kml_parser.time_format

    def _init_from_fit(self):
        """
        Initialise GPX instance from FIT file.
        """
        fit_parser = FitParser(self.source)
        self.gpx = fit_parser.gpx
        self._precisions = fit_parser.precisions
        self._time_format = fit_parser.time_format

    def _init_from_dataframe(self, source: IntoFrameT):
        """
        Initialise GPX instance from Dataframe.
        """
        self.gpx = Gpx.from_dataframe(source)

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
        return self.gpx.name()

    def set_name(self, new_name: str) -> None:
        """
        Set activity name.

        Args:
            new_name (str): New activity name.
        """
        self.gpx.set_name(new_name)

    ###############################################################################
    #### Points ###################################################################
    ###############################################################################

    def nb_points(self) -> int:
        """
        Return the number of points in the GPX.
        """
        return self.gpx.nb_points()

    def bounds(self) -> Tuple[float, float, float, float]:
        """
        Find the bounding coordinates of the activity.

        Returns:
            Tuple[float, float, float, float]: Min latitude, min
                longitude, max latitude, max longitude.
        """
        return self.gpx.bounds()

    def center(self) -> Tuple[float, float]:
        """
        Find the center coordinates of the activity.

        Returns:
            Tuple[float, float]: Latitude and longitude of the center
                point.
        """
        return self.gpx.center()

    def first_point(self) -> WayPoint:  # TODO remove?
        """
        Return the first point of the activity.
        """
        return self.gpx.first_point()

    def last_point(self) -> WayPoint:  # TODO remove?
        """
        Return the last point of the activity.
        """
        return self.gpx.last_point()

    def extreme_points(
        self,
    ) -> Tuple[WayPoint, WayPoint, WayPoint, WayPoint]:  # TODO remove?
        """
        Find extreme points in track, i.e.: points with lowest and
        highest latitude and longitude.

        Returns:
            Tuple[WayPoint, WayPoint, WayPoint, WayPoint]: Min latitude
                point, min longitude point, max latitude point, max
                longitude points.
        """
        return self.gpx.extreme_points()

    ###############################################################################
    #### Distance and Elevation ###################################################
    ###############################################################################

    def distance(self) -> float:
        """
        Returns the distance (in meters) of the activity.
        """
        return self.gpx.distance()

    def ascent(self) -> float:
        """
        Returns the ascent (in meters) of the activity.
        """
        return self.gpx.ascent()

    def descent(self) -> float:
        """
        Returns the descent (in meters) of the activity.
        """
        return self.gpx.descent()

    def min_elevation(self) -> float:
        """
        Returns the minimum elevation (in meters) of the activity.
        """
        return self.gpx.min_elevation()

    def max_elevation(self) -> float:
        """
        Returns the maximum elevation (in meters) of the activity.
        """
        return self.gpx.max_elevation()

    def compute_points_ascent_rate(self) -> None:  # TODO Do automatically in Gpx?
        """
        Compute ascent rate at each point.
        """
        self.gpx.compute_points_ascent_rate()

    def min_ascent_rate(self) -> float:  # TODO rename to max_descent_rate?
        """
        Return the minimum ascent rate of the activity.
        """
        return self.gpx.min_ascent_rate()

    def max_ascent_rate(self) -> float:
        """
        Return the maximum ascent rate of the activity.
        """
        return self.gpx.max_ascent_rate()

    ###############################################################################
    #### Time #####################################################################
    ###############################################################################

    def start_time(self) -> datetime:
        """
        Return the start time of the activity.
        """
        return self.gpx.start_time()

    def stop_time(self) -> datetime:
        """
        Return the stop time of the activity.
        """
        return self.gpx.stop_time()

    def total_elapsed_time(self) -> datetime:
        """
        Return the total elapsed time during the activity.
        """
        return self.gpx.total_elapsed_time()

    def stopped_time(self) -> datetime:
        """
        Return the stopped time during the activity.
        """
        return self.gpx.stopped_time()

    def moving_time(self) -> datetime:
        """
        Return the moving time during the activity.
        """
        return self.gpx.moving_time()

    ###############################################################################
    #### Speed and Pace ###########################################################
    ###############################################################################

    def avg_speed(self) -> float:
        """
        Return average speed (in kilometers per hour) of the activity.
        """
        return self.gpx.avg_speed()

    def avg_moving_speed(self) -> float:
        """
        Return average moving speed (in kilometers per hour) during the activity.
        """
        return self.gpx.avg_moving_speed()

    def compute_points_speed(self) -> None:  # TODO remove?
        """
        Compute speed (in kilometers per hour) at each track point.
        """
        self.gpx.compute_points_speed()

    def min_speed(self) -> float:
        """
        Return the minimum speed (in kilometers per hour)during the activity.
        """
        return self.gpx.min_speed()

    def max_speed(self) -> float:
        """
        Return the maximum speed (in kilometers per hour) during the activity.
        """
        return self.gpx.max_speed()

    def avg_pace(self) -> float:
        """
        Return average pace (in minutes per kilometer) during the activity.
        """
        return self.gpx.avg_pace()

    def avg_moving_pace(self) -> float:
        """
        Return average moving pace (in minutes per kilometer) during the activity.
        """
        return self.gpx.avg_moving_pace()

    def compute_points_pace(self) -> None:  # TODO remove?
        """
        Compute pace at each track point.
        """
        self.gpx.compute_points_pace()

    def min_pace(self) -> float:
        """
        Return the minimum pace (in minutes per kilometer) during the activity.
        """
        return self.gpx.min_pace()

    def max_pace(self) -> float:
        """
        Return the maximum pace (in minutes per kilometer) during the activity.
        """
        return self.gpx.max_pace()

    def compute_points_ascent_speed(self) -> None:  # TODO remove?
        """
        Compute ascent speed (in kilometers per hour) at each track point.
        """
        self.gpx.compute_points_ascent_speed()

    def min_ascent_speed(self) -> float:
        """
        Return the minimum ascent speed (in kilometers per hour) during the activity.
        """
        return self.gpx.min_ascent_speed()

    def max_ascent_speed(self) -> float:
        """
        Return the maximum ascent speed (in kilometers per hour) during the activity.
        """
        return self.gpx.max_ascent_speed()

    ###############################################################################
    #### Data Removal #############################################################
    ###############################################################################

    def remove_metadata(self):
        """
        Remove metadata.
        """
        self.gpx.remove_metadata()

    def remove_elevation(self):
        """
        Remove elevation data.
        """
        self.gpx.remove_elevation()

    def remove_time(self):
        """
        Remove time data.
        """
        self.gpx.remove_time()

    def remove_extensions(self):
        """
        Remove extensions data.
        """
        self.gpx.remove_extensions()

    ###############################################################################
    #### Error Correction #########################################################
    ###############################################################################

    def remove_gps_errors(self):
        """
        Remove GPS errors.
        """
        self.gpx.remove_gps_errors()

    def remove_close_points(
        self, min_dist: float = 1, max_dist: float = 10
    ):  # TODO remove?
        """
        Remove points that are to close together.

        Args:
            min_dist (float, optional): Minimal distance between two
                points. Defaults to 1.
            max_dist (float, optional): Maximal distance between two
                points. Defaults to 10.
        """
        self.gpx.remove_close_points(min_dist, max_dist)

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
        self.gpx.simplify(epsilon)

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
        values: List[str] = None,
        as_series: bool = False,
    ) -> Dict:
        """
        Convert GPX object to dictionary.

        Args:
            values (List[str], optional): List of values to write.
                Supported values: "lat", "lon", "ele", "time", "speed",
                "pace", "ascent_rate", "ascent_speed",
                "distance_from_start". Defaults to None.
            as_series (bool, optional): True -> Values are Series False
                -> Values are List[Any]. Defaults to False.

        Returns:
            Dict: Return a dictionary representing the GPX.
        """
        return self.gpx.to_dict(values, as_series)

    def to_pandas(self, values: List[str] = None) -> pd.DataFrame:
        """
        Convert GPX object to Pandas Dataframe.

        Args:
            values (List[str], optional): List of values to write.
                Supported values: "lat", "lon", "ele", "time", "speed",
                "pace", "ascent_rate", "ascent_speed",
                "distance_from_start". Defaults to None.

        Returns:
            pd.DataFrame: Return a dictionary representing the GPX.
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

        return self.gpx.to_pandas(values)

    def to_polars(self, values: List[str] = None) -> pl.DataFrame:
        """
        Convert GPX object to Polars Dataframe.

        Args:
            values (List[str], optional): List of values to write.
                Supported values: "lat", "lon", "ele", "time", "speed",
                "pace", "ascent_rate", "ascent_speed",
                "distance_from_start". Defaults to None.

        Returns:
            pl.DataFrame: Return a dictionary representing the GPX.
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

        return self.gpx.to_polars(values)

    def to_csv(
        self,
        dest: Optional[str | Path | IO[str] | IO[bytes] | bytes] = None,
        values: List[str] = None,
        **kwargs,
    ) -> Union[str, None]:
        """
        Write the GPX object track coordinates to a CSV file.

        Args:
            dest (str | Path | IO[str] | IO[bytes] | bytes, optional):
                Path to a file or a file-like object to write in.
                Defaults to None.
            values (List[str], optional): List of values to write.
                Supported values: "lat", "lon", "ele", "time", "speed",
                "pace", "ascent_rate", "ascent_speed",
                "distance_from_start". Defaults to None.

        Returns:
            Union[str, None]: CSV like string if path is set to None.
        """
        return self.gpx.to_csv(dest, values, **kwargs)

    def to_gpx(
        self,
        dest: Optional[str | Path | IO[str] | IO[bytes] | bytes] = None,
        *,
        properties: bool = True,
        bounds_fields: Optional[List[str]] = None,
        copyright_fields: Optional[List[str]] = None,
        email_fields: Optional[List[str]] = None,
        extensions_fields: Optional[Dict] = None,
        gpx_fields: Optional[List[str]] = None,
        link_fields: Optional[List[str]] = None,
        metadata_fields: Optional[List[str]] = None,
        person_fields: Optional[List[str]] = None,
        point_segment_fields: Optional[List[str]] = None,
        point_fields: Optional[List[str]] = None,
        route_fields: Optional[List[str]] = None,
        track_segment_fields: Optional[List[str]] = None,
        track_fields: Optional[List[str]] = None,
        way_point_fields: Optional[List[str]] = None,
        track_point_fields: Optional[List[str]] = None,
        mandatory_fields: bool = True,
    ) -> Union[str, None]:
        """
        Write the GPX object to a GPX file.

        Args:
            dest (str | Path | IO[str] | IO[bytes] | bytes, optional):
                Path to a file or a file-like object to write in.
                Defaults to None.
            properties (bool, optional): _description_. Defaults to True.
            bounds_fields (Optional[List[str]], optional): _description_. Defaults to None.
            copyright_fields (Optional[List[str]], optional): _description_. Defaults to None.
            email_fields (Optional[List[str]], optional): _description_. Defaults to None.
            extensions_fields (Optional[Dict], optional): _description_. Defaults to None.
            gpx_fields (Optional[List[str]], optional): _description_. Defaults to None.
            link_fields (Optional[List[str]], optional): _description_. Defaults to None.
            metadata_fields (Optional[List[str]], optional): _description_. Defaults to None.
            person_fields (Optional[List[str]], optional): _description_. Defaults to None.
            point_segment_fields (Optional[List[str]], optional): _description_. Defaults to None.
            point_fields (Optional[List[str]], optional): _description_. Defaults to None.
            route_fields (Optional[List[str]], optional): _description_. Defaults to None.
            track_segment_fields (Optional[List[str]], optional): _description_. Defaults to None.
            track_fields (Optional[List[str]], optional): _description_. Defaults to None.
            way_point_fields (Optional[List[str]], optional): _description_. Defaults to None.
            track_point_fields (Optional[List[str]], optional): _description_. Defaults to None.
            mandatory_fields (bool, optional): _description_. Defaults to True.

        Returns:
            Union[str, None]: GPX like string if path is set to None.
        """
        bounds_fields = bounds_fields if bounds_fields is not None else Bounds.fields
        copyright_fields = (
            copyright_fields if copyright_fields is not None else Copyright.fields
        )
        email_fields = email_fields if email_fields is not None else Email.fields
        default_extensions_fields = (
            self._gpx_parser.extensions_fields if self._gpx_parser is not None else {}
        )
        extensions_fields = (
            extensions_fields
            if extensions_fields is not None
            else default_extensions_fields
        )
        gpx_fields = gpx_fields if gpx_fields is not None else Gpx.fields
        link_fields = link_fields if link_fields is not None else Link.fields
        metadata_fields = (
            metadata_fields if metadata_fields is not None else Metadata.fields
        )
        person_fields = person_fields if person_fields is not None else Person.fields
        point_segment_fields = (
            point_segment_fields
            if point_segment_fields is not None
            else PointSegment.fields
        )
        point_fields = point_fields if point_fields is not None else Point.fields
        route_fields = route_fields if route_fields is not None else Route.fields
        track_segment_fields = (
            track_segment_fields
            if track_segment_fields is not None
            else TrackSegment.fields
        )
        track_fields = track_fields if track_fields is not None else Track.fields
        way_point_fields = (
            way_point_fields if way_point_fields is not None else WayPoint.fields
        )
        track_point_fields = (
            track_point_fields if track_point_fields is not None else WayPoint.fields
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
            way_point_fields=way_point_fields,
            track_point_fields=track_point_fields,
            mandatory_fields=mandatory_fields,
        )

    def to_kml(
        self,
        dest: Optional[str | Path | IO[str] | IO[bytes] | bytes] = None,
        *,
        styles: Optional[List[Tuple[str, Dict]]] = None,
    ) -> Union[str, None]:
        """
        Write the GPX object to a KML file.

        Args:
            dest (str | Path | IO[str] | IO[bytes] | bytes, optional):
                Path to a file or a file-like object to write in.
                Defaults to None.
            styles (Optional[List[Tuple[str, Dict]]], optional): KML
                styles. Defaults to None.

        Returns:
            Union[str, None]: KML like string if path is set to None.
        """
        return self._kml_writer.write(dest, styles)
