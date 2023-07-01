import os
from typing import Optional, Union
import logging
import xml.etree.ElementTree as ET

from ..gpx_elements import Bounds, Copyright, Email, Extensions, Gpx, Link, Metadata, Person, TrackPoint, TrackSegment, Track

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
            waypoints: bool = True,
            ele: bool = True,
            time: bool = True,
            precisions: dict = None) -> None:
        """
        Initialize Writer instance.

        Args:
            gpx (Gpx, optional): Gpx instance to write. Defaults to None.
            path (str, optional): Path to the file to write. Defaults to "".
            properties (bool, optional): Toggle properties writting. Defaults to True.
            metadata (bool, optional): Toggle metadata writting. Defaults to True.
            waypoint (bool, optional): Toggle way points writting. Defaults to True.
            ele (bool, optional): Toggle elevation writting. Defaults to True.
            time (bool, optional): Toggle time writting. Defaults to True.
            precisions (dict, optional): Decimal precision for each type of value. Defaults to None.
        """
        self.gpx: Gpx = gpx
        self.path: str = path
        self.gpx_string: str = ""

        # Parameters
        self.properties: bool = properties
        self.metadata: bool = metadata
        self.waypoints: bool = waypoints
        self.ele: bool = ele
        self.time: bool = time

        self.precisions: dict = precisions

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
        Add bounds element to GPX element.

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
        Add copyright element to GPX element.

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
        Add email element to GPX element.

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
        Add extensions element to GPX element.

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
        Add link element to GPX element.

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
        Add person element to GPX element.

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
    
    def properties_to_string(self, gpx_root: ET.Element) -> ET.Element:

        logging.info("Preparing properties...")

        if self.gpx.creator in ["eTrex 32x"]:
            return self.properties_to_string_garmin(gpx_root)
        elif self.gpx.creator in ["StravaGPX"]:
            return self.properties_to_string_strava(gpx_root)
        else:
            return self.properties_to_string_garmin(gpx_root) # Default to Garmin style

    def properties_to_string_garmin(self, gpx_root: ET.Element) -> ET.Element:

        gpx_root.set("xmlns", self.gpx.xmlns)
        gpx_root.set("creator", self.gpx.creator)
        gpx_root.set("version", self.gpx.version)
        schema_location_string = ""
        for loc in self.gpx.xsi_schema_location:
            schema_location_string += loc
            schema_location_string += " "
        schema_location_string = schema_location_string[:len(schema_location_string)-1]
        gpx_root.set("xsi:schemaLocation", schema_location_string)

        return gpx_root
    
    def properties_to_string_strava(self, gpx_root: ET.Element) -> ET.Element:

        gpx_root.set("creator", self.gpx.creator)
        schema_location_string = ""
        for loc in self.gpx.xsi_schema_location:
            schema_location_string += loc
            schema_location_string += " "
        schema_location_string = schema_location_string[:len(schema_location_string)-1]
        gpx_root.set("xsi:schemaLocation", schema_location_string)
        gpx_root.set("version", self.gpx.version)
        gpx_root.set("xmlns", self.gpx.xmlns)
        
        return gpx_root

    def metadata_to_string(self, gpx_root: ET.Element) -> ET.Element:
        
        logging.info("Preparing metadata...")

        metadata = ET.SubElement(gpx_root, "metadata")

        metadata, _ = self.add_subelement(metadata, "name", self.gpx.metadata.name)
        metadata, _ = self.add_subelement(metadata, "desc", self.gpx.metadata.desc)
        metadata = self.add_person(metadata, self.gpx.metadata.author)
        metadata = self.add_copyright(metadata, self.gpx.metadata.copyright)
        metadata = self.add_link(metadata, self.gpx.metadata.link)
        metadata, _ = self.add_subelement(metadata, "time", self.gpx.metadata.time.strftime("%Y-%m-%dT%H:%M:%SZ"))
        metadata, _ = self.add_subelement(metadata, "keywords", self.gpx.metadata.keywords)
        metadata = self.add_bounds(metadata, self.gpx.metadata.bounds)
        metadata = self.add_extensions(metadata, self.gpx.metadata.extensions)

        return gpx_root
    
    def waypoints_to_string(self, gpx_root: ET.Element) -> ET.Element:

        logging.info("Preparing way points...")

        for gpx_way_point in self.gpx.wpt:
            way_point = ET.SubElement(gpx_root, "wpt")
            way_point.set("lat", "{:.{}f}".format(gpx_way_point.lat, self.precisions["lat_lon"]))
            way_point.set("lon", "{:.{}f}".format(gpx_way_point.lon, self.precisions["lat_lon"]))
            if gpx_way_point.ele is not None:
                ele = ET.SubElement(way_point, "ele")
                ele.text = "{:.{}f}".format(gpx_way_point.ele, self.precisions["elevation"])
            if gpx_way_point.time is not None:
                time = ET.SubElement(way_point, "time")
                time.text = gpx_way_point.time.strftime("%Y-%m-%dT%H:%M:%SZ")
            if gpx_way_point.mag_var is not None:
                mag_var = ET.SubElement(way_point, "magvar")
                mag_var.text = "{:.{}f}".format(gpx_way_point.mag_var, self.precisions["default"])
            if gpx_way_point.geo_id_height is not None:
                geo_id_height = ET.SubElement(way_point, "geoidheight")
                geo_id_height.text = "{:.{}f}".format(gpx_way_point.geo_id_height, self.precisions["default"])
            if gpx_way_point.name is not None:
                name = ET.SubElement(way_point, "name")
                name.text = gpx_way_point.name
            if gpx_way_point.cmt is not None:
                cmt = ET.SubElement(way_point, "cmt")
                cmt.text = gpx_way_point.cmt
            if gpx_way_point.desc is not None:
                desc = ET.SubElement(way_point, "desc")
                desc.text = gpx_way_point.desc
            if gpx_way_point.src is not None:
                src = ET.SubElement(way_point, "src")
                src.text = gpx_way_point.src
            if gpx_way_point.link is not None:
                way_point = self.add_link(way_point, gpx_way_point.link)
            if gpx_way_point.sym is not None:
                sym = ET.SubElement(way_point, "sym")
                sym.text = gpx_way_point.sym
            if gpx_way_point.type is not None:
                type = ET.SubElement(way_point, "type")
                type.text = gpx_way_point.type
            if gpx_way_point.fix is not None:
                fix = ET.SubElement(way_point, "fix")
                fix.text = gpx_way_point.fix
            if gpx_way_point.sat is not None:
                sat = ET.SubElement(way_point, "sat")
                sat.text = str(gpx_way_point.sat)
            if gpx_way_point.hdop is not None:
                hdop = ET.SubElement(way_point, "hdop")
                hdop.text = "{:.{}f}".format(gpx_way_point.hdop, self.precisions["default"])
            if gpx_way_point.vdop is not None:
                vdop = ET.SubElement(way_point, "vdop")
                vdop.text = "{:.{}f}".format(gpx_way_point.vdop, self.precisions["default"])
            if gpx_way_point.pdop is not None:
                pdop = ET.SubElement(way_point, "pdop")
                pdop.text = "{:.{}f}".format(gpx_way_point.pdop, self.precisions["default"])
            if gpx_way_point.age_of_gps_data is not None:
                age_of_gps_data = ET.SubElement(way_point, "age_of_gps_data")
                age_of_gps_data.text = "{:.{}f}".format(gpx_way_point.age_of_gps_data, self.precisions["default"])
            if gpx_way_point.dgpsid is not None:
                dgpsid = ET.SubElement(way_point, "dgpsid")
                dgpsid.text = str(gpx_way_point.dgpsid)
            if gpx_way_point.extensions is not None:
                way_point = self.add_extensions(way_point, gpx_way_point.extensions)

        return gpx_root
    
    def tracks_to_string(self, gpx_root: ET.Element) -> ET.Element:

        logging.info("Preparing tracks...")

        for gpx_track in self.gpx.tracks:
            track = ET.SubElement(gpx_root, "trk")
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
                        time.text = gpx_point.time.strftime("%Y-%m-%dT%H:%M:%SZ")

        return gpx_root

    def gpx_to_string(self) -> str:

        if self.gpx is not None:
            logging.info("Start convertion from GPX to string")
            # Reset string
            self.gpx_string = ""

            # Root
            gpx_root = ET.Element("gpx")

            # Properties
            if self.properties:
                gpx_root = self.properties_to_string(gpx_root)

            # Metadata
            if self.metadata:
                gpx_root = self.metadata_to_string(gpx_root)

            # Way points
            if self.waypoints:
                gpx_root = self.waypoints_to_string(gpx_root)

            # Tracks
            gpx_root = self.tracks_to_string(gpx_root)

            # Convert data to string
            logging.info("Converting GPX to string...")
            self.gpx_string = ET.tostring(gpx_root, encoding="unicode")
            # self.gpx_string = ET.tostring(gpx_root, encoding="utf-8")


            logging.info(f"GPX successfully converted to string\n{self.gpx_string}")

            return self.gpx_string

    def write_gpx(self):
        
        # Write GPX file
        with open(self.path, "w") as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
            f.write(self.gpx_string)

    def write(self, path: str):
        
        directory_path = os.path.dirname(os.path.realpath(path))
        logging.debug(directory_path)
        if not os.path.exists(directory_path):
            logging.error("Provided path does not exist")
            return
        
        self.path = path
        self.gpx_to_string()
        self.write_gpx()

