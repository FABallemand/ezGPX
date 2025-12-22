"""
This module contains the FitParser class.
"""

import warnings
from datetime import datetime
from pathlib import Path
from typing import IO, List

from fitparse import FitFile

from ..constants.precisions import DEFAULT_PRECISION, POSSIBLE_TIME_FORMATS
from ..gpx_elements import Gpx, Track, TrackSegment, WayPoint
from .parser import Parser


class FitParser(Parser):
    """
    Fit file parser.
    """

    _semicircles_to_deg_const = 180 / 2**31

    def __init__(self, source: str | Path | IO[str] | IO[bytes] | bytes) -> None:
        """
        Initialise FitParser instance.

        Args:
            source (str | Path | IO[str] | IO[bytes] | bytes): Path to a
                file or a file-like object to parse.
        """
        # Initialise Parser and parse FIT file
        super().__init__(source)
        self.parse()

    def _find_time_format(self, time_str):
        """
        Find the time format used in GPX file.
        Also find if the GPX file contains time data.
        """
        if time_str is None:
            self.time_data = False
            warnings.warn("No time element in FIT file.")
            return

        self.time_data = True
        for tf in POSSIBLE_TIME_FORMATS:
            try:
                datetime.strptime(time_str, tf)
                self.time_format = tf
                break
            except ValueError:
                pass
        else:
            warnings.warn(
                """Unknown time format. Default time format will be used uppon
                writting."""
            )

    def _semicircles_to_deg(self, list_: List) -> List:
        """
        Convert semicircle data from FIT file to dms data.

        Args:
            list_ (list): List of semicircle values.

        Returns:
            list: List of dms values.
        """
        return [FitParser._semicircles_to_deg_const * x for x in list_]

    def _parse(self):
        """
        Parse FIT file and store data in a Gpx element.
        """
        lat_data = []
        lon_data = []
        alt_data = []
        time_data = []

        units = {"alt": "", "lat": "", "lon": ""}

        fit_file = FitFile(self.source)

        for record in fit_file.get_messages("record"):
            for record_data in record:
                if record_data.name == "position_lat":
                    lat_data.append(record_data.value)
                    if units["lat"] == "":
                        units["lat"] = record_data.units
                        # Temporary (may change if units["lat"] == "semicircles")
                        self.precisions["lat_lon"] = self.find_precision(
                            record_data.value
                        )
                if record_data.name == "position_long":
                    lon_data.append(record_data.value)
                    if units["lon"] == "":
                        units["lon"] = record_data.units
                if record_data.name == "altitude":
                    alt_data.append(record_data.value)
                    if units["alt"] == "":
                        units["alt"] = record_data.units
                        self.precisions["elevation"] = self.find_precision(
                            record_data.value
                        )
                if record_data.name == "timestamp":
                    time_data.append(record_data.value)
                    self._find_time_format(record_data.value)

        # Convert semicircles data to radians ??
        if units["lat"] == "semicircles":
            self.precisions["lat_lon"] = DEFAULT_PRECISION
            lat_data = self._semicircles_to_deg(lat_data)
        if units["lon"] == "semicircles":
            lon_data = self._semicircles_to_deg(lon_data)

        # Store FIT data in Gpx element
        trkpt = [
            WayPoint("trkpt", lat, lon, alt, time)
            for lat, lon, alt, time in zip(lat_data, lon_data, alt_data, time_data)
        ]
        trkseg = TrackSegment(trkpt=trkpt)
        trk = Track(trkseg=[trkseg])
        self.gpx.trk = [trk]

    def _add_properties(self):
        self.gpx.creator = "ezGPX"
        self.gpx.xmlns = "http://www.topografix.com/GPX/1/1"
        self.gpx.version = "1.1"
        self.gpx.xmlns_xsi = "http://www.w3.org/2001/XMLSchema-instance"
        self.gpx.xsi_schema_location = [
            "http://www.topografix.com/GPX/1/1",
            "http://www.topografix.com/GPX/1/1/gpx.xsd",
        ]

    def parse(self) -> Gpx:
        """
        Parse Fit file.

        Returns:
            Gpx: Gpx instance.
        """
        # Parse FIT file
        self._parse()

        # Add properties
        self._add_properties()

        return self.gpx
