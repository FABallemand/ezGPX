from __future__ import annotations
import errno
import logging
import os
import warnings
from datetime import datetime
from math import degrees
from typing import Dict, List, Optional, Tuple, Union, Type
from zipfile import ZipFile
import pandas as pd

from ..gpx_elements import (Bounds, Copyright, Email, Extensions, Gpx, Link,
                            Metadata, Person, Point, PointSegment, Route,
                            Track, TrackSegment, WayPoint)
from ..parsers.fit_parser import FitParser
from ..parsers.gpx_parser import GPXParser
from ..parsers.kml_parser import KMLParser
from ..utils import EARTH_RADIUS
from ..writers.gpx_writer import GPXWriter
from ..writers.kml_writer import KMLWriter

# GPX = NewType("GPX", object)  # GPX forward declaration for type hint


class GPX():
    """
    High level GPX object.
    """
    TIME_RELATED_VALUES = ["time", "speed", "pace", "ascent_speed"]
    ELEVATION_RELATED_VALUES = ["ele", "ascent_rate", "ascent_speed"]

    def __init__(
            self,
            file_path: Optional[str] = None,
            xml_schema: bool = True,
            xml_extensions_schemas: bool = False) -> None:
        """
        Initialise GPX instance.

        Parameters
        ----------
        file_path : Optional[str], optional
            Path to the file to parse, by default None
        xml_schema : bool, optional
            Toggle schema verification during parsing, by default True
        extensions_schemas : bool, optional
            Toggle extensions schema verificaton during parsing, by default False
        """
        # GPX file description
        self.file_path: str = None
        self.file_name: str = None

        # GPX file content
        self.gpx: Gpx = None
        self._ele_data: bool = False
        self._time_data: bool = False
        self._precisions: Dict = None
        self._time_format: str = None

        # Parsers
        self._gpx_parser: GPXParser = None
        self._kml_parser: KMLParser = None
        self._fit_parser: FitParser = None

        # Utility attributes
        self._dataframe: pd.DataFrame = None

        # Valid file
        if isinstance(file_path, str) and os.path.exists(file_path):
            self.file_path = file_path
            self.file_name = os.path.basename(file_path)

            # GPX
            if file_path.endswith(".gpx"):
                self._gpx_parser = GPXParser(
                    file_path, xml_schema, xml_extensions_schemas)
                self.gpx = self._gpx_parser.gpx
                self._ele_data = self._gpx_parser.ele_data
                self._time_data = self._gpx_parser.time_data
                self._precisions = self._gpx_parser.precisions
                self._time_format = self._gpx_parser.time_format

            # KML
            elif file_path.endswith(".kml"):
                self._kml_parser = KMLParser(
                    file_path, xml_schema, xml_extensions_schemas)
                self.gpx = self._kml_parser.gpx
                self._precisions = self._kml_parser.precisions
                self._time_format = self._kml_parser.time_format

            # KMZ
            elif file_path.endswith(".kmz"):
                kmz = ZipFile(file_path, 'r')
                kmls = [info.filename for info in kmz.infolist(
                ) if info.filename.endswith(".kml")]
                if "doc.kml" not in kmls:
                    raise FileNotFoundError(f"Unable to parse file: {file_path}"
                        "Expected to find doc.kml inside KMZ file.")
                kml = kmz.open("doc.kml", 'r').read()
                self._write_tmp_kml("tmp.kml", kml)
                self._kml_parser = KMLParser(
                    "tmp.kml", xml_schema, xml_extensions_schemas)
                self.gpx = self._kml_parser.gpx
                self._precisions = self._kml_parser.precisions
                self._time_format = self._kml_parser.time_format
                os.remove("tmp.kml")

            # FIT
            elif file_path.endswith(".fit"):
                self._fit_parser = FitParser(file_path)
                self.gpx = self._fit_parser.gpx
                self._precisions = self._fit_parser.precisions
                self._time_format = self._fit_parser.time_format

            # NOT SUPPORTED
            else:
                raise ValueError(f"Unable to parse this type of file: {file_path}"
                                 "Consider renaming your file with the proper file extension.")

            # Writers
            self._gpx_writer: GPXWriter = GPXWriter(self.gpx, self._precisions,
                                                    self._time_format)
            self._kml_writer: KMLWriter = KMLWriter(self.gpx,
                                                    precisions=self._precisions,
                                                    time_format=self._time_format)

        # Invalid file path
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), file_path)

    def _write_tmp_kml(
            self,
            path: str = "tmp.kml",
            kml_string: Optional[bytes] = None):
        """
        Write temproray .KML file in order to parse KMZ file.
        """
        # Open/create KML file
        try:
            f = open(path, "wb")
        except OSError:
            logging.exception("Could not open/read file: %s", path)
            raise
        # Write KML file
        with f:
            if kml_string is not None:
                f.write(kml_string)

    def __str__(self) -> str:
        return self._gpx_writer.gpx_to_string()

    def __repr__(self):
        return f"file_path = {self.file_path}\ngpx = {self.gpx}"

###############################################################################
#### Schemas ##################################################################
###############################################################################

    def check_xml_schema(self) -> bool:
        """
        Check XML schema.

        Returns
        -------
        bool
            True if the file follows XML schemas.
        """
        return self.gpx.check_xml_schema(self.file_path)

    def check_xml_extensions_schemas(self) -> bool:
        """
        Check XML extension schemas.

        Returns
        -------
        bool
            True if the file follows XML schemas.
        """
        return self.gpx.check_xml_extensions_schemas(self.file_path)

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
        return self.gpx.name()

    def set_name(self, new_name: str) -> None:
        """
        Set name.

        Parameters
        ----------
        new_name : str
            New name.
        """
        self.gpx.set_name(new_name)

###############################################################################
#### Points ###################################################################
###############################################################################

    def nb_points(self) -> int:
        """
        Return the number of points in the GPX.

        Returns
        -------
        int
            Number of points in the GPX.
        """
        return self.gpx.nb_points()

    def bounds(self) -> Tuple[float, float, float, float]:
        """
        Find minimum and maximum latitude and longitude.

        Returns
        -------
        Tuple[float, float, float, float]
            Min latitude, min longitude, max latitude, max longitude.
        """
        return self.gpx.bounds()

    def center(self) -> Tuple[float, float]:
        """
        Return the coordinates of the center point.

        Returns
        -------
        Tuple[float, float]
            Latitude and longitude of the center point.
        """
        return self.gpx.center()

    def first_point(self) -> WayPoint:
        """
        Return GPX first point.

        Returns
        -------
        WayPoint
            First point.
        """
        return self.gpx.first_point()

    def last_point(self) -> WayPoint:
        """
        Return GPX last point.

        Returns
        -------
        WayPoint
            Last point.
        """
        return self.gpx.last_point()

    def extreme_points(self) -> Tuple[WayPoint, WayPoint, WayPoint, WayPoint]:
        """
        Find extreme points in track, i.e.: points with lowest and highest latitude and longitude.

        Returns
        -------
        Tuple[WayPoint, WayPoint, WayPoint, WayPoint]
            Min latitude point, min longitude point, max latitude point, max longitude point
        """
        return self.gpx.extreme_points()

###############################################################################
#### Distance and Elevation ###################################################
###############################################################################

    def distance(self) -> float:
        """
        Returns the distance (meters) of tracks contained in the GPX.

        Returns
        -------
        float
            Distance (meters).
        """
        return self.gpx.distance()

    def ascent(self) -> float:
        """
        Returns the ascent (meters) of tracks contained in the GPX.

        Returns
        -------
        float
            Ascent (meters).
        """
        return self.gpx.ascent()

    def descent(self) -> float:
        """
        Returns the descent (meters) of tracks contained in the GPX.

        Returns
        -------
        float
            Descent (meters).
        """
        return self.gpx.descent()

    def min_elevation(self) -> float:
        """
        Returns the minimum elevation (meters) in tracks contained in the GPX.

        Returns
        -------
        float
            Minimum elevation (meters).
        """
        return self.gpx.min_elevation()

    def max_elevation(self) -> float:
        """
        Returns the maximum elevation (meters) in tracks contained in the GPX.

        Returns
        -------
        float
            Maximum elevation (meters).
        """
        return self.gpx.max_elevation()

    def compute_points_ascent_rate(self) -> None:
        """
        Compute ascent rate at each point.
        """
        self.gpx.compute_points_ascent_rate()

    def min_ascent_rate(self) -> float:
        """
        Return activity minimum ascent rate.

        Returns
        -------
        float
            Minimum ascent rate.
        """
        return self.gpx.min_ascent_rate()

    def max_ascent_rate(self) -> float:
        """
        Return activity maximum ascent rate.

        Returns
        -------
        float
            Maximum ascent rate.
        """
        return self.gpx.max_ascent_rate()

###############################################################################
#### Time #####################################################################
###############################################################################

    def start_time(self) -> datetime:
        """
        Return the activity start time.

        Returns
        -------
        datetime
            Start time.
        """
        return self.gpx.start_time()

    def stop_time(self) -> datetime:
        """
        Return the activity stop time.

        Returns
        -------
        datetime
            Stop time.
        """
        return self.gpx.stop_time()

    def total_elapsed_time(self) -> datetime:
        """
        Return the total elapsed time during the activity.

        Returns
        -------
        datetime
            Total elapsed time.
        """
        return self.gpx.total_elapsed_time()

    def stopped_time(self) -> datetime:
        """
        Return the stopped time during the activity.

        Returns
        -------
        datetime
            Stopped time.
        """
        return self.gpx.stopped_time()

    def moving_time(self) -> datetime:
        """
        Return the moving time during the activity.

        Returns
        -------
        datetime
            Moving time.
        """
        return self.gpx.moving_time()

###############################################################################
#### Speed and Pace ###########################################################
###############################################################################

    def avg_speed(self) -> float:
        """
        Return average speed (kilometres per hour) during the activity.

        Returns
        -------
        float
            Average speed (kilometres per hour).
        """
        return self.gpx.avg_speed()

    def avg_moving_speed(self) -> float:
        """
        Return average moving speed (kilometres per hour) during the activity.

        Returns
        -------
        float
            Average moving speed (kilometres per hour).
        """
        return self.gpx.avg_moving_speed()

    def compute_points_speed(self) -> None:
        """
        Compute speed (kilometres per hour) at each track point.
        """
        self.gpx.compute_points_speed()

    def min_speed(self) -> float:
        """
        Return the minimum speed during the activity.

        Returns
        -------
        float
            Minimum speed.
        """
        return self.gpx.min_speed()

    def max_speed(self) -> float:
        """
        Return the maximum speed during the activity.

        Returns
        -------
        float
            Maximum speed.
        """
        return self.gpx.max_speed()

    def avg_pace(self) -> float:
        """
        Return average pace (minutes per kilometer) during the activity.

        Returns
        -------
        float
            Average pace (minutes per kilometer).
        """
        return self.gpx.avg_pace()

    def avg_moving_pace(self) -> float:
        """
        Return average moving pace (minutes per kilometer) during the activity.

        Returns
        -------
        float
            Average moving pace (minutes per kilometer).
        """
        return self.gpx.avg_moving_pace()

    def compute_points_pace(self) -> None:
        """
        Compute pace at each track point.
        """
        self.gpx.compute_points_pace()

    def min_pace(self) -> float:
        """
        Return the minimum pace during the activity.

        Returns
        -------
        float
            Minimum pace.
        """
        return self.gpx.min_pace()

    def max_pace(self) -> float:
        """
        Return the maximum pace during the activity.

        Returns
        -------
        float
            Maximum pace.
        """
        return self.gpx.max_pace()

    def compute_points_ascent_speed(self) -> None:
        """
        Compute ascent speed (kilometres per hour) at each track point.
        """
        self.gpx.compute_points_ascent_speed()

    def min_ascent_speed(self) -> float:
        """
        Return the minimum ascent speed (kilometres per hour) during the activity.

        Returns
        -------
        float
            Minimum ascent speed.
        """
        return self.gpx.min_ascent_speed()

    def max_ascent_speed(self) -> float:
        """
        Return the maximum ascent speed (kilometres per hour) during the activity.

        Returns
        -------
        float
            Maximum ascent speed.
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
        self.gpx.remove_close_points(min_dist, max_dist)

###############################################################################
#### Simplification ###########################################################
###############################################################################

    def simplify(self, tolerance: float = 2):
        """
        Simplify tracks using Ramer-Douglas-Peucker algorithm.

        Parameters
        ----------
        tolerance : float, optional
            Tolerance (meters). Corresponds to the minimum distance between the
            point and the track before the point is removed, by default 2
        """
        epsilon = degrees(tolerance/EARTH_RADIUS)
        self.gpx.simplify(epsilon)

###############################################################################
#### Merge ####################################################################
###############################################################################

    @staticmethod
    def merge(gpx_1: GPX, gpx_2: GPX) -> GPX:
        """
        Merge GPX objects in a new instance.

        Parameters
        ----------
        gpx_1 : GPX
            First GPX object
        gpx_2 : GPX
            Second GPX object

        Returns
        -------
        GPX
            Merged GPX (new instance)
        """
        topo = ["http://www.topografix.com/GPX/1/1", "http://www.topografix.com/GPX/1/1/gpx.xsd"]

        # Create new GPX instance
        merged_gpx = GPX()

        # Fill new GPX instance
        merged_gpx.gpx.tag = "gpx"
        merged_gpx.gpx.xmlns = "http://www.topografix.com/GPX/1/1"
        merged_gpx.gpx.xsi_schema_location = list(
            set(topo + gpx_1.gpx.xsi_schema_location
                + gpx_2.gpx.xsi_schema_location))
        merged_gpx.gpx.version = "1.1"
        merged_gpx.gpx.creator = "ezGPX"
        merged_gpx.gpx.metadata = (gpx_2.gpx.metadata
                                   if gpx_1.gpx.metadata is None
                                   else gpx_1.gpx.metadata)
        merged_gpx.gpx.wpt = gpx_1.gpx.wpt + gpx_2.gpx.wpt
        merged_gpx.gpx.rte = gpx_1.gpx.rte + gpx_2.gpx.rte
        merged_gpx.gpx.trk = gpx_1.gpx.trk + gpx_2.gpx.trk
        merged_gpx.gpx.extensions = Extensions(
            "extensions", gpx_1.gpx.metadata | gpx_2.gpx.metadata)

        # Return new GPX instance
        return merged_gpx

###############################################################################
#### Exports ##################################################################
###############################################################################

    def to_dict(
            self, values: List[str] = None, orient: str = "dict",
            into: Type[dict] = dict, index: bool = True) -> Dict:
        """
        Convert GPX object to dictionary.
        Pandas.DataFrame.to_dict documentation: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_dict.html

        Parameters
        ----------
        values : List[str], optional
            values : List[str], optional
            List of values to write, by default None
            Supported values: "lat", "lon", "ele", "time", "speed", "pace",
            "ascent_rate", "ascent_speed", "distance_from_start"
        orient : str, optional
            Same as in Pandas.DataFrame.to_dict, by default "dict"
        into : Type[dict], optional
            Same as in Pandas.DataFrame.to_dict, by default dict
        index : bool, optional
            Same as in Pandas.DataFrame.to_dict, by default True

        Returns
        -------
        Dict
            Return a dictionary representing the GPX. The resulting
            transformation depends on the `orient` parameter.
        """
        return self.gpx.to_dict(values, orient, into, index)

    def to_pandas(self, values: List[str] = None) -> pd.DataFrame:
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
        # Disable time related values if no time data available
        if not self._time_data:
            if any(v in GPX.TIME_RELATED_VALUES for v in values):
                warnings.warn(f"Trying to create dataframe from GPX file {self.file_path} which does not contain time data"
                              "Time related values (time, speed, pace, ascent speed) will not be present in the dataframe.",
                              UserWarning)
            for v in GPX.TIME_RELATED_VALUES:
                if v in values:
                    values.remove(v)

        # Disable elevation related values if no elevation data available
        if not self._ele_data:
            if any(v in GPX.ELEVATION_RELATED_VALUES for v in values):
                warnings.warn(f"Trying to create dataframe from GPX file {self.file_path} which does not contain elevation data"
                              "Time related values (elevation, ascent rate, ascent speed) will not be present in the dataframe.",
                              UserWarning)
            for v in GPX.ELEVATION_RELATED_VALUES:
                if v in values:
                    values.remove(v)

        return self.gpx.to_pandas(values)
    
    def to_polars(self, values: List[str] = None) -> pd.DataFrame:
        """
        Convert GPX object to Polars Dataframe.
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
        # Disable time related values if no time data available
        if not self._time_data:
            if any(v in GPX.TIME_RELATED_VALUES for v in values):
                warnings.warn(f"Trying to create dataframe from GPX file {self.file_path} which does not contain time data"
                              "Time related values (time, speed, pace, ascent speed) will not be present in the dataframe.",
                              UserWarning)
            for v in GPX.TIME_RELATED_VALUES:
                if v in values:
                    values.remove(v)

        # Disable elevation related values if no elevation data available
        if not self._ele_data:
            if any(v in GPX.ELEVATION_RELATED_VALUES for v in values):
                warnings.warn(f"Trying to create dataframe from GPX file {self.file_path} which does not contain elevation data"
                              "Time related values (elevation, ascent rate, ascent speed) will not be present in the dataframe.",
                              UserWarning)
            for v in GPX.ELEVATION_RELATED_VALUES:
                if v in values:
                    values.remove(v)

        return self.gpx.to_polars(values)

    def to_csv(
            self,
            path: str = None,
            values: List[str] = None,
            sep: str = ",",
            header: bool = True,
            index: bool = False) -> Union[str, None]: # TODO: select pandas vs polars
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
        return self.gpx.to_csv(path, values, sep, header, index)

    def to_gpx(
            self,
            path: str,
            properties: bool = True,
            bounds_fields: List[str] = None,
            copyright_fields: List[str] = None,
            email_fields: List[str] = None,
            extensions_fields: Dict = None,
            gpx_fields: List[str] = None,
            link_fields: List[str] = None,
            metadata_fields: List[str] = None,
            person_fields: List[str] = None,
            point_segment_fields: List[str] = None,
            point_fields: List[str] = None,
            route_fields: List[str] = None,
            track_segment_fields: List[str] = None,
            track_fields: List[str] = None,
            way_point_fields: List[str] = None,
            track_point_fields: List[str] = None,
            xml_schema: bool = True,
            xml_extensions_schemas: bool = False) -> bool:
        """
        Write the GPX object to a .gpx file.

        Parameters
        ----------
        path : str
            Path to the new .gpx file.
        xml_schema : bool, optional
            Toggle schema verification after writting, by default True
        xml_extensions_schemas : bool, optional
            Toggle extensions schema verificaton after writing. Requires internet connection and is not guaranted to work, by default False

        Returns
        -------
        bool
            Return False if written file does not follow checked schemas. Return True otherwise.
        """
        bounds_fields = (bounds_fields
                         if bounds_fields is not None
                         else Bounds.fields)
        copyright_fields = (copyright_fields
                            if copyright_fields is not None
                            else Copyright.fields)
        email_fields = (email_fields
                        if email_fields is not None
                        else Email.fields)
        extensions_fields = (extensions_fields
                             if extensions_fields is not None
                             else self._gpx_parser.extensions_fields)
        gpx_fields = (gpx_fields
                      if gpx_fields is not None
                      else Gpx.fields)
        link_fields = (link_fields
                       if link_fields is not None
                       else Link.fields)
        metadata_fields = (metadata_fields
                           if metadata_fields is not None
                           else Metadata.fields)
        person_fields = (person_fields
                         if person_fields is not None
                         else Person.fields)
        point_segment_fields = (point_segment_fields
                                if point_segment_fields is not None
                                else PointSegment.fields)
        point_fields = (point_fields
                        if point_fields is not None
                        else Point.fields)
        route_fields = (route_fields
                        if route_fields is not None
                        else Route.fields)
        track_segment_fields = (track_segment_fields
                                if track_segment_fields is not None
                                else TrackSegment.fields)
        track_fields = (track_fields
                        if track_fields is not None
                        else Track.fields)
        way_point_fields = (way_point_fields
                            if way_point_fields is not None
                            else WayPoint.fields)
        track_point_fields = (track_point_fields
                              if track_point_fields is not None
                              else WayPoint.fields)
        return self._gpx_writer.write(file_path=path,
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
                                      xml_schema=xml_schema,
                                      xml_extensions_schemas=xml_extensions_schemas)

    def to_kml(
            self,
            path: str,
            styles: Optional[List[Tuple[str, Dict]]] = None,
            xml_schema: bool = True) -> bool:
        """
        Write the GPX object to a .kml file.

        Parameters
        ----------
        path : str
            Path to the .gpx file.
        styles : List[Tuple[str, Dict]], optional
            List of (style_id, style) tuples, by default None
        xml_schema : bool, optional
            Toggle schema verification after writting, by default True

        Returns
        -------
        bool
            Return False if written file does not follow checked schemas. Return True otherwise.
        """
        return self._kml_writer.write(path, styles, xml_schema)
