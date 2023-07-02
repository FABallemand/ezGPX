import os
from typing import Optional, Union
import logging
import xml.etree.ElementTree as ET

from ..gpx_elements import Bounds, Copyright, Email, Extensions, Gpx, Link, Metadata, Person, Route, TrackPoint, TrackSegment, Track, WayPoint
from ..gpx_parser import DEFAULT_PRECISION

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

    def add_subelement(self, element: ET.Element, sub_element: str, text: str = None) -> tuple[ET.Element, Union[ET.Element, None]]:
        """
        Add sub-element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            sub_element (str): GPX sub-element.
            text (str): GPX sub-element text. Defaults to None.

        Returns:
            tuple[xml.etree.ElementTree.Element, Union[xml.etree.ElementTree.Element, None]]: GPX element and GPX sub-element (if not None).
        """
        sub_element_ = None
        if text is not None:
            sub_element_ = ET.SubElement(element, sub_element)
            sub_element_.text = text
        return element, sub_element_
    
    def add_subelement_number(self, element: ET.Element, sub_element: str, number: Union[int, float] = None, precision: int = DEFAULT_PRECISION) -> tuple[ET.Element, Union[ET.Element, None]]:
        """
        Add sub-element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            sub_element (str): GPX sub-element.
            number (Union[int, float], optional): GPX sub-element value. Defaults to None.
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
                logging.error("Invalid number type")
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
            bounds_ = ET.SubElement(element, "bounds")
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
            copyright_ = ET.SubElement(element, "copyright")
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
            email_ = ET.SubElement(element, "email")
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
            extensions_ = ET.SubElement(element, "extensions")
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
            link_ = ET.SubElement(element, "link")
            if link.href is not None:
                link_.set("href", link.href)
            link_, _ = self.add_subelement(link_, "text", link.text)
            link_, _ = self.add_subelement(link_, "type", link.type)
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
            person_ = ET.SubElement(element, "person")
            person_, _ = self.add_subelement(person_, "name", person.name)
            person_ = self.add_email(person_, person.email)
            person_ = self.add_link(person_, person.link)
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
        return self.add_way_point_(element, way_point)
    
    def add_route_point(self, element: ET.Element, way_point: WayPoint) -> ET.Element:
        """
        Add WayPoint instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            route_point (WayPoint): WayPoint instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self.add_way_point_(element, way_point, "rtept")
    
    def add_way_point_(self, element: ET.Element, way_point: WayPoint, tag: str = "wpt") -> ET.Element:
        """
        Add WayPoint instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            way_point (WayPoint): WayPoint instance to add.
            tag (str, Optional): Tag to assign to the point (wpt or rtept). Defaults to "wpt".

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        way_point_ = ET.SubElement(element, tag)
        way_point_.set("lat", "{:.{}f}".format(way_point.lat, self.precisions["lat_lon"]))
        way_point_.set("lon", "{:.{}f}".format(way_point.lon, self.precisions["lat_lon"]))
        if way_point.ele is not None:
            ele = ET.SubElement(way_point_, "ele")
            ele.text = "{:.{}f}".format(way_point.ele, self.precisions["elevation"])
        if way_point.time is not None:
            time = ET.SubElement(way_point_, "time")
            time.text = way_point.time.strftime(self.time_format)
        if way_point.mag_var is not None:
            mag_var = ET.SubElement(way_point_, "magvar")
            mag_var.text = "{:.{}f}".format(way_point.mag_var, self.precisions["default"])
        if way_point.geo_id_height is not None:
            geo_id_height = ET.SubElement(way_point_, "geoidheight")
            geo_id_height.text = "{:.{}f}".format(way_point.geo_id_height, self.precisions["default"])
        if way_point.name is not None:
            name = ET.SubElement(way_point_, "name")
            name.text = way_point.name
        if way_point.cmt is not None:
            cmt = ET.SubElement(way_point_, "cmt")
            cmt.text = way_point.cmt
        if way_point.desc is not None:
            desc = ET.SubElement(way_point_, "desc")
            desc.text = way_point.desc
        if way_point.src is not None:
            src = ET.SubElement(way_point_, "src")
            src.text = way_point.src
        if way_point.link is not None:
            way_point = self.add_link(way_point_, way_point.link)
        if way_point.sym is not None:
            sym = ET.SubElement(way_point_, "sym")
            sym.text = way_point.sym
        if way_point.type is not None:
            type = ET.SubElement(way_point_, "type")
            type.text = way_point.type
        if way_point.fix is not None:
            fix = ET.SubElement(way_point_, "fix")
            fix.text = way_point.fix
        if way_point.sat is not None:
            sat = ET.SubElement(way_point_, "sat")
            sat.text = str(way_point.sat)
        if way_point.hdop is not None:
            hdop = ET.SubElement(way_point_, "hdop")
            hdop.text = "{:.{}f}".format(way_point.hdop, self.precisions["default"])
        if way_point.vdop is not None:
            vdop = ET.SubElement(way_point_, "vdop")
            vdop.text = "{:.{}f}".format(way_point.vdop, self.precisions["default"])
        if way_point.pdop is not None:
            pdop = ET.SubElement(way_point_, "pdop")
            pdop.text = "{:.{}f}".format(way_point.pdop, self.precisions["default"])
        if way_point.age_of_gps_data is not None:
            age_of_gps_data = ET.SubElement(way_point_, "age_of_gps_data")
            age_of_gps_data.text = "{:.{}f}".format(way_point.age_of_gps_data, self.precisions["default"])
        if way_point.dgpsid is not None:
            dgpsid = ET.SubElement(way_point_, "dgpsid")
            dgpsid.text = str(way_point.dgpsid)
        if way_point.extensions is not None:
            way_point = self.add_extensions(way_point_, way_point.extensions)

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
    
    def add_properties_strava(self) -> None:
        """
        Add Strava style properties to the GPX root element.
        """
        self.gpx_root.set("creator", self.gpx.creator)
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

        metadata = ET.SubElement(self.gpx_root, "metadata")

        metadata, _ = self.add_subelement(metadata, "name", self.gpx.metadata.name)
        metadata, _ = self.add_subelement(metadata, "desc", self.gpx.metadata.desc)
        metadata = self.add_person(metadata, self.gpx.metadata.author)
        metadata = self.add_copyright(metadata, self.gpx.metadata.copyright)
        metadata = self.add_link(metadata, self.gpx.metadata.link)
        metadata, _ = self.add_subelement(metadata, "time", self.gpx.metadata.time.strftime(self.time_format))
        metadata, _ = self.add_subelement(metadata, "keywords", self.gpx.metadata.keywords)
        metadata = self.add_bounds(metadata, self.gpx.metadata.bounds)
        metadata = self.add_extensions(metadata, self.gpx.metadata.extensions)
    
    def add_root_way_points(self) -> None:
        """
        Add wpt elements to the GPX root element.
        """
        logging.info("Preparing way points...")

        for gpx_way_point in self.gpx.wpt:
            self.gpx_root = self.add_way_point(self.gpx_root, gpx_way_point)
    
    def add_root_routes(self) -> None:
        """
        Add rte elements to the GPX root element.
        """
        logging.info("Preparing routes...")

        for gpx_route in self.gpx.rte:
            route = ET.SubElement(self.gpx_root, "rte")
            if gpx_route.name is not None:
                name = ET.SubElement(route, "name")
                name.text = gpx_route.name
            if gpx_route.cmt is not None:
                cmt = ET.SubElement(route, "cmt")
                cmt.text = gpx_route.cmt
            if gpx_route.desc is not None:
                desc = ET.SubElement(route, "desc")
                desc.text = gpx_route.desc
            if gpx_route.src is not None:
                src = ET.SubElement(route, "src")
                src.text = gpx_route.src
            if gpx_route.link is not None:
                route = self.add_link(route, gpx_route.link)
            if gpx_route.number is not None:
                number = ET.SubElement(route, "number")
                number.text = str(gpx_route.number)
            if gpx_route.type is not None:
                type = ET.SubElement(route, "type")
                type.text = gpx_route.type
            if gpx_route.extensions is not None:
                route = self.add_extensions(route, gpx_route.extensions)
            if gpx_route.rtept is not []:
                for way_point in gpx_route.rtept:
                    route = self.add_route_point(route, way_point)
    
    def add_root_tracks(self,) -> None:
        """
        Add trck elements to the GPX root element.
        """
        logging.info("Preparing tracks...")

        for gpx_track in self.gpx.tracks:
            track = ET.SubElement(self.gpx_root, "trk")
            track, _ = self.add_subelement(track, "name", gpx_track.name)

            # Track segments
            for gpx_segment in gpx_track.trkseg:
                segment = ET.SubElement(track, "trkseg")

                # Track points
                for gpx_point in gpx_segment.trkpt:
                    point = ET.SubElement(segment, "trkpt")
                    point.set("lat", "{:.{}f}".format(gpx_point.latitude, self.precisions["lat_lon"]))
                    point.set("lon", "{:.{}f}".format(gpx_point.longitude, self.precisions["lat_lon"]))
                    if self.ele and gpx_point.elevation is not None:
                        ele = ET.SubElement(point, "ele")
                        ele.text = "{:.{}f}".format(gpx_point.elevation, self.precisions["elevation"])
                    if self.time and gpx_point.time is not None:
                        time = ET.SubElement(point, "time")
                        time.text = gpx_point.time.strftime(self.time_format)
    
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

            logging.info(f"GPX successfully converted to string\n{self.gpx_string}")

            return self.gpx_string

    def write_gpx(self):
        """
        Convert Gpx instance to string and write to file.
        """
        # Write GPX file
        with open(self.path, "w") as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
            f.write(self.gpx_string)

    def write(self, path: str):
        """
        Handle writing.

        Args:
            path (str): Path to write the GPX file.
        """
        directory_path = os.path.dirname(os.path.realpath(path))
        logging.debug(directory_path)
        if not os.path.exists(directory_path):
            logging.error("Provided path does not exist")
            return
        
        self.path = path
        self.gpx_to_string()
        self.write_gpx()

