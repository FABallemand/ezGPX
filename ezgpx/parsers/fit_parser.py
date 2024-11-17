import os
from typing import Optional, List
import logging
from datetime import datetime

from fitparse import FitFile

from .parser import Parser, DEFAULT_PRECISION
from ..gpx_elements import Gpx, TrackSegment, Track, WayPoint


class FitParser(Parser):
    """
    Fit file parser.
    """

    def __init__(self, file_path: Optional[str] = None) -> None:
        """
        Initialize FitParser instance.

        Args:
            file_path (str, optional): Path to the file to parse. Defaults to None.
        """
        if not (file_path.endswith(".fit") or file_path.endswith(".FIT")):
            return
        super().__init__(file_path)

        if self.file_path is not None and os.path.exists(self.file_path):
            self.parse()
        else:
            logging.warning("File path does not exist")

    def _set_time_format(self, time):
        """
        Set the time format used in FIT file. 
        """
        if time is None:
            logging.warning("No time element in FIT file.")
            return

        try:
            datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
            self.time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        except:
            self.time_format = "%Y-%m-%dT%H:%M:%SZ"  # default time format

    def _semicircles_to_deg(self, l: List) -> List:
        """
        Convert semicircle data from FIT file to dms data.

        Args:
            l (list): List of semicircle values.

        Returns:
            list: List of dms values.
        """
        const = 180 / 2**31
        l = map(lambda x: const * x, l)
        return l

    def _parse(self):
        """
        Parse FIT file and store data in a Gpx element.
        """
        lat_data = []
        lon_data = []
        alt_data = []
        time_data = []

        units = {"alt": "", "lat": "", "lon": ""}

        fit_file = FitFile(self.file_path)

        for record in fit_file.get_messages("record"):
            for record_data in record:
                if record_data.name == "position_lat":
                    lat_data.append(record_data.value)
                    if units["lat"] == "":
                        units["lat"] = record_data.units
                        # Temporary (may change if units["lat"] == "semicircles")
                        self.precisions["lat_lon"] = self.find_precision(
                            record_data.value)
                if record_data.name == "position_long":
                    lon_data.append(record_data.value)
                    if units["lon"] == "":
                        units["lon"] = record_data.units
                if record_data.name == "altitude":
                    alt_data.append(record_data.value)
                    if units["alt"] == "":
                        units["alt"] = record_data.units
                        self.precisions["elevation"] = self.find_precision(
                            record_data.value)
                if record_data.name == "timestamp":
                    time_data.append(record_data.value)
                    self._set_time_format(record_data.value)

        # Convert semicircles data to radians ??
        if units["lat"] == "semicircles":
            self.precisions["lat_lon"] = DEFAULT_PRECISION
            lat_data = self._semicircles_to_deg(lat_data)
        if units["lon"] == "semicircles":
            lon_data = self._semicircles_to_deg(lon_data)

        # Store FIT data in Gpx element
        trkpt = []
        for lat, lon, alt, time in list(zip(lat_data, lon_data, alt_data, time_data)):
            trkpt.append(WayPoint("trkpt", lat, lon, alt, time))
        trkseg = TrackSegment(trkpt=trkpt)
        trk = Track(trkseg=[trkseg])
        self.gpx.trk = [trk]

    def _add_properties(self):
        self.gpx.creator = "ezGPX"
        self.gpx.xmlns = "http://www.topografix.com/GPX/1/1"
        self.gpx.version = "1.1"
        self.gpx.xmlns_xsi = "http://www.w3.org/2001/XMLSchema-instance"
        self.gpx.xsi_schema_location = [
            "http://www.topografix.com/GPX/1/1", "http://www.topografix.com/GPX/1/1/gpx.xsd"]

    def parse(self) -> Gpx:
        """
        Parse Fit file.

        Returns:
            Gpx: Gpx instance.
        """
        # Parse FIT file
        try:
            self._parse()
        except Exception as err:
            logging.exception("Unexpected %s, %s.\n"
                              "Unable to parse FIT file.", err, type(err))
            raise

        # Add properties
        self._add_properties()

        logging.debug("Parsing complete!!")
        return self.gpx
