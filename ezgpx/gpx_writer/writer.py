import os
from typing import Optional, Union
import logging
import xml.etree.ElementTree as ET
from datetime import datetime

from ..gpx_elements import Bounds, Copyright, Email, Extensions, Gpx, Link, Metadata, Person, PointSegment, Point, Route, TrackSegment, Track, WayPoint
from ..gpx_parser import DEFAULT_PRECISION, DEFAULT_TIME_FORMAT

class Writer():
    """
    GPX file writer.
    """

    def __init__(
            self,
            gpx: Gpx = None,
            path: str = "",
            properties: bool = True,
            metadata: bool = True,
            way_points: bool = True,
            routes: bool = True,
            extensions: bool = True,
            ele: bool = True,
            time: bool = True,
            precisions: dict = None,
            time_format: str = None) -> None:
        """
        Initialize Writer instance.

        Args:
            gpx (Gpx, optional): Gpx instance to write. Defaults to None.
            path (str, optional): Path to the file to write. Defaults to "".
            properties (bool, optional): Toggle properties writting. Defaults to True.
            metadata (bool, optional): Toggle metadata writting. Defaults to True.
            way_point (bool, optional): Toggle way points writting. Defaults to True.
            routes (bool, optional): Toggle routes writting. Defaults to True.
            extensions (bool, optional): Toggle extensions writting. Defaults to True.
            ele (bool, optional): Toggle elevation writting. Defaults to True.
            time (bool, optional): Toggle time writting. Defaults to True.
            precisions (dict, optional): Decimal precision for each type of value. Defaults to None.
            time_format (dict, optional): Time format. Defaults to None.
        """
        self.gpx: Gpx = gpx
        self.path: str = path
        self.gpx_string: str = ""

        # Parameters
        self.properties: bool = properties
        self.metadata: bool = metadata
        self.way_points: bool = way_points
        self.routes: bool = routes
        self.extensions: bool = extensions
        self.ele: bool = ele
        self.time: bool = time

        self.precisions: dict = precisions
        self.time_format = time_format

        self.gpx_root = None

    def add_subelement(self, element: ET.Element, sub_element: str, text: str) -> tuple[ET.Element, Union[ET.Element, None]]:
        """
        Add sub-element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            sub_element (str): GPX sub-element.
            text (str): GPX sub-element text.

        Returns:
            tuple[xml.etree.ElementTree.Element, Union[xml.etree.ElementTree.Element, None]]: GPX element and GPX sub-element (if not None).
        """
        sub_element_ = None
        if text is not None:
            sub_element_ = ET.SubElement(element, sub_element)
            sub_element_.text = text
        return element, sub_element_
    
    def add_subelement_number(self, element: ET.Element, sub_element: str, number: Union[int, float], precision: int = DEFAULT_PRECISION) -> tuple[ET.Element, Union[ET.Element, None]]:
        """
        Add sub-element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            sub_element (str): GPX sub-element.
            number (Union[int, float], optional): GPX sub-element value.
            precision (int, optional): Precision. Defaults to DEFAULT_PRECISION.

        Returns:
            tuple[xml.etree.ElementTree.Element, Union[xml.etree.ElementTree.Element, None]]: GPX element and GPX sub-element (if not None).
        """
        sub_element_ = None
        if number is not None:
            sub_element_ = ET.SubElement(element, sub_element)
            if type(number) is int:
                sub_element_.text = str(number)
            elif type(number) is float:
                sub_element_.text = "{:.{}f}".format(number, precision)
            else:
                logging.error("Invalid number type.")
        return element, sub_element_
    
    def add_subelement_time(self, element: ET.Element, sub_element: str, time: datetime, format: str = DEFAULT_TIME_FORMAT) -> ET.Element:
        """
        Add sub-element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            sub_element (str): GPX sub-element.
            time (datetime, optional): GPX sub-element value.
            format (str, optional): Format. Defaults to DEFAULT_TIME_FORMAT.

        Returns:
            tuple[xml.etree.ElementTree.Element, Union[xml.etree.ElementTree.Element, None]]: GPX element and GPX sub-element (if not None).
        """
        sub_element_ = None
        if time is not None:
            sub_element_ = ET.SubElement(element, sub_element)
            try:
                sub_element_.text = time.strftime(format)
            except:
                logging.error("Invalid time format.")
        return element, sub_element_
    
    def add_bounds(self, element: ET.Element, bounds: Bounds) -> ET.Element:
        """
        Add Bounds instance to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            bounds (Bounds): Bounds instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        if bounds is not None:
            bounds_ = ET.SubElement(element, bounds.tag)
            bounds_, _ = self.add_subelement_number(bounds_, "minlat", bounds.minlat, self.precisions["lat_lon"])
            bounds_, _ = self.add_subelement_number(bounds_, "minlon", bounds.minlon, self.precisions["lat_lon"])
            bounds_, _ = self.add_subelement_number(bounds_, "maxlat", bounds.maxlat, self.precisions["lat_lon"])
            bounds_, _ = self.add_subelement_number(bounds_, "maxlon", bounds.maxlon, self.precisions["lat_lon"])
        return element
    
    def add_copyright(self, element: ET.Element, copyright: Copyright) -> ET.Element:
        """
        Add Copyright instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            copyright (Copyright): Copyright instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        if copyright is not None:
            copyright_ = ET.SubElement(element, copyright.tag)
            if copyright.author is not None:
                copyright_.set("author", copyright.author)
            copyright_, _ = self.add_subelement(copyright_, "year", str(copyright.year))
            copyright_, _ = self.add_subelement(copyright_, "licence", str(copyright.licence))
        return element
    
    def add_email(self, element: ET.Element, email: Email) -> ET.Element:
        """
        Add Email instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            email (Email): Email instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        if email is not None:
            email_ = ET.SubElement(element, email.tag)
            if email.id is not None:
                email_.set("id", email.id)
            if email.domain is not None:
                email_.set("domain", email.domain)
        return element

    def add_extensions(self, element: ET.Element, extensions: Extensions) -> ET.Element:
        """
        Add Extensions instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            extensions (Extensions): Extensions instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        if extensions is not None:
            extensions_ = ET.SubElement(element, extensions.tag)
            extensions_, _ = self.add_subelement(extensions_, "display_color", extensions.display_color)
            extensions_, _ = self.add_subelement_number(extensions_, "distance", extensions.distance, self.precisions["distance"])
            extensions_, _ = self.add_subelement_number(extensions_, "total_elapsed_time", extensions.total_elapsed_time, self.precisions["duration"])
            extensions_, _ = self.add_subelement_number(extensions_, "moving_time", extensions.moving_time, self.precisions["duration"])
            extensions_, _ = self.add_subelement_number(extensions_, "stopped_time", extensions.stopped_time, self.precisions["duration"])
            extensions_, _ = self.add_subelement_number(extensions_, "moving_speed", extensions.moving_speed, self.precisions["speed"])
            extensions_, _ = self.add_subelement_number(extensions_, "max_speed", extensions.max_speed, self.precisions["speed"])
            extensions_, _ = self.add_subelement_number(extensions_, "max_elevation", extensions.max_elevation, self.precisions["elevation"])
            extensions_, _ = self.add_subelement_number(extensions_, "min_elevation", extensions.min_elevation, self.precisions["elevation"])
            extensions_, _ = self.add_subelement_number(extensions_, "ascent", extensions.ascent, self.precisions["elevation"])
            extensions_, _ = self.add_subelement_number(extensions_, "descent", extensions.descent, self.precisions["elevation"])
            extensions_, _ = self.add_subelement_number(extensions_, "avg_ascent_rate", extensions.avg_ascent_rate, self.precisions["rate"])
            extensions_, _ = self.add_subelement_number(extensions_, "max_ascent_rate", extensions.max_descent_rate, self.precisions["rate"])
            extensions_, _ = self.add_subelement_number(extensions_, "avg_descent_rate", extensions.avg_descent_rate, self.precisions["rate"])
            extensions_, _ = self.add_subelement_number(extensions_, "max_descent_rate", extensions.max_descent_rate, self.precisions["rate"])
        return element
    
    def add_link(self, element: ET.Element, link: Link) -> ET.Element:
        """
        Add Link instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            link (Link): Link instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        if link is not None:
            link_ = ET.SubElement(element, link.tag)
            if link.href is not None:
                link_.set("href", link.href)
            link_, _ = self.add_subelement(link_, "text", link.text)
            link_, _ = self.add_subelement(link_, "type", link.type)
        return element

    def add_metadata(self, element: ET.Element, metadata: Metadata) -> ET.Element:
        """
        Add Metadata instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            metadata (Metadata): Metadata instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        if metadata is not None:
            metadata_ = ET.SubElement(self.gpx_root, metadata.tag)
            metadata_, _ = self.add_subelement(metadata_, "name", metadata.name)
            metadata_, _ = self.add_subelement(metadata_, "desc", metadata.desc)
            metadata_ = self.add_person(metadata_, metadata.author)
            metadata_ = self.add_copyright(metadata_, metadata.copyright)
            metadata_ = self.add_link(metadata_, metadata.link)
            metadata_, _ = self.add_subelement_time(metadata_, "time", metadata.time, self.time_format)
            metadata_, _ = self.add_subelement(metadata_, "keywords", metadata.keywords)
            metadata_ = self.add_bounds(metadata_, metadata.bounds)
            metadata_ = self.add_extensions(metadata_, metadata.extensions)
        return element
    
    def add_person(self, element: ET.Element, person: Person) -> ET.Element:
        """
        Add Person instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            person (Person): Person instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        if person is not None:
            person_ = ET.SubElement(element, person.tag)
            person_, _ = self.add_subelement(person_, "name", person.name)
            person_ = self.add_email(person_, person.email)
            person_ = self.add_link(person_, person.link)
        return element
    
    def add_point_segment(self, element: ET.Element, point_segment: PointSegment) -> ET.Element:
        """
        Add PointSegment instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            point_segment (PointSegment): PointSegment instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        if point_segment is not None:
            pass
        return element

    def add_point(self, element: ET.Element, point: Point) -> ET.Element:
        """
        Add Point instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            point (Point): Point instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        if point is not None:
            point_ = ET.SubElement(element, point.tag)
            if point.lat is not None:
                point_.set("lat", "{:.{}f}".format(point.lat, self.precisions["lat_lon"]))
            if point.lon is not None:
                point_.set("lon", "{:.{}f}".format(point.lon, self.precisions["lat_lon"]))
            point_ = self.add_subelement_number(point_, "ele", point.ele, self.precisions["elevation"])
            point_, _ = self.add_subelement_time(point_, "time", point.time, self.time_format)
        return element

    def add_route(self, element: ET.Element, route: Route) -> ET.Element:
        """
        Add Route instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            route (Route): Route instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        if route is not None:
            route_ = ET.SubElement(element, route.tag)
            route_, _ = self.add_subelement(route_, "name", route.name)
            route_, _ = self.add_subelement(route_, "cmt", route.cmt)
            route_, _ = self.add_subelement(route_, "desc", route.desc)
            route_, _ = self.add_subelement(route_, "src", route.src)
            route_ = self.add_link(route_, route.link)
            route_, _ = self.add_subelement_number(route_, "number", route.src, 0)
            route_, _ = self.add_subelement(route_, "type", route.type)
            route_ = self.add_extensions(route_, route.extensions)
            for way_point in route.rtept:
                route_ = self.add_way_point(route_, way_point)
        return element

    def add_track_segment(self, element: ET.Element, track_segment: TrackSegment) -> ET.Element:
        """
        Add TrackSegment instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            track_segment (TrackSegment): TrackSegment instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        if track_segment is not None:
            track_segment_ = ET.SubElement(element, track_segment.tag)
            for track_point in track_segment.trkpt:
                track_segment_ = self.add_way_point(track_segment_, track_point)
        return element

    def add_track(self, element: ET.Element, track: Track) -> ET.Element:
        """
        Add Track instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            track (Track): Track instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        if track is not None:
            track_ = ET.SubElement(element, track.tag)
            track_, _ = self.add_subelement(track_, "name", track.name)
            for track_segment in track.trkseg:
                track_ = self.add_track_segment(track_, track_segment)
        return element
    
    def add_way_point(self, element: ET.Element, way_point: WayPoint) -> ET.Element:
        """
        Add WayPoint instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            way_point (WayPoint): WayPoint instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        if way_point is not None:
            way_point_ = ET.SubElement(element, way_point.tag)
            way_point_.set("lat", "{:.{}f}".format(way_point.lat, self.precisions["lat_lon"]))
            way_point_.set("lon", "{:.{}f}".format(way_point.lon, self.precisions["lat_lon"]))
            way_point_, _ = self.add_subelement_number(way_point_, "ele", way_point.ele, self.precisions["elevation"])
            way_point_, _ = self.add_subelement_time(way_point_, "time", way_point.time, self.time_format)
            way_point_, _ = self.add_subelement_number(way_point_, "magvar", way_point.mag_var, self.precisions["default"])
            way_point_, _ = self.add_subelement_number(way_point_, "geoidheight", way_point.geo_id_height, self.precisions["default"])
            way_point_, _ = self.add_subelement(way_point_, "name", way_point.name)
            way_point_, _ = self.add_subelement(way_point_, "cmt", way_point.cmt)
            way_point_, _ = self.add_subelement(way_point_, "desc", way_point.desc)
            way_point_, _ = self.add_subelement(way_point_, "src", way_point.src)
            way_point_ = self.add_link(way_point_, way_point.link)
            way_point_, _ = self.add_subelement(way_point_, "src", way_point.src)
            way_point_, _ = self.add_subelement(way_point_, "type", way_point.type)
            way_point_, _ = self.add_subelement(way_point_, "fix", way_point.fix)
            way_point_, _ = self.add_subelement_number(way_point_, "sat", way_point.sat, 0)
            way_point_, _ = self.add_subelement_number(way_point_, "hdop", way_point.hdop, self.precisions["default"])
            way_point_, _ = self.add_subelement_number(way_point_, "vdop", way_point.vdop, self.precisions["default"])
            way_point_, _ = self.add_subelement_number(way_point_, "pdop", way_point.pdop, self.precisions["default"])
            way_point_, _ = self.add_subelement_number(way_point_, "ageofgpsdata", way_point.age_of_gps_data, self.precisions["default"])
            way_point_, _ = self.add_subelement_number(way_point_, "dgpsid", way_point.dgpsid, 0)
            way_point_ = self.add_extensions(way_point_, way_point.extensions)
        return element
         
    def add_properties_garmin(self) -> None:
        """
        Add Garmin style properties to the GPX root element.
        """
        self.gpx_root.set("xmlns", self.gpx.xmlns)
        self.gpx_root.set("creator", self.gpx.creator)
        self.gpx_root.set("version", self.gpx.version)
        schema_location_string = ""
        for loc in self.gpx.xsi_schema_location:
            schema_location_string += loc
            schema_location_string += " "
        schema_location_string = schema_location_string[:len(schema_location_string)-1]
        self.gpx_root.set("xsi:schemaLocation", schema_location_string)
        self.gpx_root.set("xmlns:xsi", self.gpx.xmlns_xsi)
    
    def add_properties_strava(self) -> None:
        """
        Add Strava style properties to the GPX root element.
        """
        self.gpx_root.set("creator", self.gpx.creator)
        self.gpx_root.set("xmlns:xsi", self.gpx.xmlns_xsi)
        schema_location_string = ""
        for loc in self.gpx.xsi_schema_location:
            schema_location_string += loc
            schema_location_string += " "
        schema_location_string = schema_location_string[:len(schema_location_string)-1]
        self.gpx_root.set("xsi:schemaLocation", schema_location_string)
        self.gpx_root.set("version", self.gpx.version)
        self.gpx_root.set("xmlns", self.gpx.xmlns)
    
    def add_root_properties(self) -> None:
        """
        Add properties to the GPX root element.
        """
        logging.info("Preparing properties...")

        if self.gpx.creator in ["eTrex 32x"]:
             self.add_properties_garmin()
        elif self.gpx.creator in ["StravaGPX"]:
             self.add_properties_strava()
        else:
             self.add_properties_garmin() # Default to Garmin style

    def add_root_metadata(self) -> None:
        """
        Add metadata element to the GPX root element.
        """
        logging.info("Preparing metadata...")

        self.gpx_root = self.add_metadata(self.gpx_root, self.gpx.metadata)
    
    def add_root_way_points(self) -> None:
        """
        Add wpt elements to the GPX root element.
        """
        logging.info("Preparing way points...")

        for way_point in self.gpx.wpt:
            self.gpx_root = self.add_way_point(self.gpx_root, way_point)
    
    def add_root_routes(self) -> None:
        """
        Add rte elements to the GPX root element.
        """
        logging.info("Preparing routes...")

        for route in self.gpx.rte:
            self.gpx_root = self.add_route(self.gpx_root, route)
    
    def add_root_tracks(self) -> None:
        """
        Add trck elements to the GPX root element.
        """
        logging.info("Preparing tracks...")

        for track in self.gpx.tracks:
            self.gpx_root = self.add_track(self.gpx_root, track)
    
    def add_root_extensions(self) -> None:
        """
        Add extensions element to the GPX root element.
        """
        logging.info("Preparing extensions...")

        if self.gpx.extensions is not None:
            self.gpx_root = self.add_extensions(self.gpx_root, self.gpx.extensions)

    def gpx_to_string(self) -> str:
        """
        Convert Gpx instance to string.

        Returns:
            str: String corresponding to the Gpx instance.
        """
        if self.gpx is not None:
            logging.info("Start convertion from GPX to string")
            # Reset string
            self.gpx_string = ""

            # Root
            self.gpx_root = ET.Element("gpx")

            # Properties
            if self.properties:
                self.add_root_properties()

            # Metadata
            if self.metadata:
                self.add_root_metadata()

            # Way points
            if self.way_points:
                self.add_root_way_points()

            # Routes
            if self.routes:
                self.add_root_routes()

            # Tracks
            self.add_root_tracks()

            # Extensions
            if self.extensions:
                self.add_root_extensions()

            # Convert data to string
            logging.info("Converting GPX to string...")
            self.gpx_string = ET.tostring(self.gpx_root, encoding="unicode")
            # self.gpx_string = ET.tostring(gpx_root, encoding="utf-8")

            logging.info(f"GPX successfully converted to string:\n{self.gpx_string}")

            return self.gpx_string

    def write_gpx(self):
        """
        Convert Gpx instance to string and write to file.
        """
        # Open/create GPX file
        try:
            f = open(self.path, "w")
        except OSError:
            logging.exception(f"Could not open/read file: {self.path}")
            raise
        # Write GPX file
        with f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
            f.write(self.gpx_string)

    def write(self, path: str):
        """
        Handle writing.

        Args:
            path (str): Path to write the GPX file.
        """
        directory_path = os.path.dirname(os.path.realpath(path))
        if not os.path.exists(directory_path):
            logging.error("Provided path does not exist")
            return
        
        self.path = path
        self.gpx_to_string()
        self.write_gpx()

