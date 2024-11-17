import os
import errno
import warnings
from typing import List, Dict
import logging
import xml.etree.ElementTree as ET

from .writer import Writer
from ..gpx_elements import (Bounds, Copyright, Email, Extensions, Gpx, Link,
                            Metadata, Person, PointSegment, Point, Route,
                            TrackSegment, Track, WayPoint)
from .gpx_writer_method_behavior_creator import GPXWriterMethodBehaviorCreator


class GPXWriter(Writer):
    """
    GPX file writer.
    """

    def __init__(
            self,
            gpx: Gpx = None,
            precisions: Dict = None,
            time_format: str = None) -> None:
        """
        Initialize GPXWriter instance.

        Args:
            gpx (Gpx, optional): Gpx instance to write. Defaults to None.
            precisions (dict, optional): Decimal precision for each type of value. Defaults to None.
            time_format (dict, optional): Time format. Defaults to None.
        """
        super().__init__(gpx)

        # Parameters
        self.precisions: Dict = precisions
        self.time_format: str = time_format

        # Utility attributes
        self.file_name: str = ""
        self.gpx_string: str = ""
        self.gpx_root = None

        # Methods behavior creator
        self.behavior_creator: GPXWriterMethodBehaviorCreator = GPXWriterMethodBehaviorCreator()

        # Methods behaviors
        self._add_bounds = self.placeholder_behavior
        self._add_copyright = self.placeholder_behavior
        self._add_email = self.placeholder_behavior
        self._add_link = self.placeholder_behavior
        self._add_metadata = self.placeholder_behavior
        self._add_person = self.placeholder_behavior
        self._add_point_segment = self.placeholder_behavior
        self._add_point = self.placeholder_behavior
        self._add_route = self.placeholder_behavior
        self._add_track_segment = self.placeholder_behavior
        self._add_track = self.placeholder_behavior
        self._add_way_point = self.placeholder_behavior
        self._add_track_point = self.placeholder_behavior

        # Fields
        self.properties: bool = None
        self.bounds_fields: List[str] = None
        self.copyright_fields: List[str] = None
        self.email_fields: List[str] = None
        self.extensions_fields: Dict = None
        self.gpx_fields: List[str] = None
        self.link_fields: List[str] = None
        self.metadata_fields: List[str] = None
        self.person_fields: List[str] = None
        self.point_segment_fields: List[str] = None
        self.point_fields: List[str] = None
        self.route_fields: List[str] = None
        self.track_segment_fields: List[str] = None
        self.track_fields: List[str] = None
        self.way_point_fields: List[str] = None
        self.track_point_fields: List[str] = None

    def placeholder_behavior(self, element, subelement):
        print(element, subelement)
        return None

    def add_bounds(self, element: ET.Element, bounds: Bounds) -> ET.Element:
        """
        Add Bounds instance to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            bounds (Bounds): Bounds instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_bounds(self, element, bounds)

    def add_copyright(self, element: ET.Element, copyright_: Copyright) -> ET.Element:
        """
        Add Copyright instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            copyright (Copyright): Copyright instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_copyright(self, element, copyright_)

    def add_email(self, element: ET.Element, email: Email) -> ET.Element:
        """
        Add Email instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            email (Email): Email instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_email(self, element, email)

    def _add_extensions_rec(self, extensions_, values, extensions_fields) -> ET.Element:
        if extensions_ is not None:
            # Add n-th level extensions
            for k0, v0 in values.items():
                if k0 in extensions_fields.keys():
                    # If k0 contains sub-elements
                    if isinstance(v0["elmts"], dict):
                        # Create sub-element
                        sub_extensions_ = ET.SubElement(extensions_, k0)

                        # Set attributes
                        for k1, v1 in v0["attrib"].items():
                            if k1 in extensions_fields[k0]["attrib"].keys():
                                self.setIfNotNone(extensions_, k1, v1)

                        # Add (n+1)-th level extensions
                        sub_extensions_ = self._add_extensions_rec(
                            sub_extensions_, v0["elmts"], extensions_fields[k0]["elmts"])
                    # Else, k0 contains a value
                    else:
                        extensions_, sub_extensions_ = self.add_subelement(
                            extensions_, k0, v0["elmts"])

                        # Set attributes
                        for k1, v1 in v0["attrib"].items():
                            if k1 in extensions_fields[k0]["attrib"].keys():
                                self.setIfNotNone(sub_extensions_, k1, v1)

        return extensions_

    def add_extensions(
            self, element: ET.Element, extensions: Extensions,
            extensions_fields: Dict) -> ET.Element:
        """
        Add Extnsions instance element to GPX element.

        Parameters
        ----------
        element : xml.etree.ElementTree.Element
            GPX element
        extensions : Extensions
            Extensions instance to add
        extensions_fields : Dict
            Extensions fileds to add

        Returns
        -------
        xml.etree.ElementTree.Element
            GPX element
        """
        if extensions is not None:
            extensions_ = ET.SubElement(element, extensions.tag)
            extensions_ = self._add_extensions_rec(
                extensions_, extensions.values, extensions_fields)
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
        return self._add_link(self, element, link)

    def add_metadata(self, element: ET.Element, metadata: Metadata) -> ET.Element:
        """
        Add Metadata instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            metadata (Metadata): Metadata instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_metadata(self, element, metadata)

    def add_person(self, element: ET.Element, person: Person) -> ET.Element:
        """
        Add Person instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            person (Person): Person instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_person(self, element, person)

    def add_point_segment(self, element: ET.Element, point_segment: PointSegment) -> ET.Element:
        """
        Add PointSegment instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            point_segment (PointSegment): PointSegment instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_point_segment(self, element, point_segment)

    def add_point(self, element: ET.Element, point: Point) -> ET.Element:
        """
        Add Point instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            point (Point): Point instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_point(self, element, point)

    def add_route(self, element: ET.Element, route: Route) -> ET.Element:
        """
        Add Route instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            route (Route): Route instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_route(self, element, route)

    def add_track_segment(self, element: ET.Element, track_segment: TrackSegment) -> ET.Element:
        """
        Add TrackSegment instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            track_segment (TrackSegment): TrackSegment instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_track_segment(self, element, track_segment)

    def add_track(self, element: ET.Element, track: Track) -> ET.Element:
        """
        Add Track instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            track (Track): Track instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_track(self, element, track)

    def add_way_point(self, element: ET.Element, way_point: WayPoint) -> ET.Element:
        """
        Add WayPoint instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            way_point (WayPoint): WayPoint instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_way_point(self, element, way_point)

    def add_track_point(self, element: ET.Element, way_point: WayPoint) -> ET.Element:
        """
        Add WayPoint instance (with trkpt tag) element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            way_point (WayPoint): WayPoint instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_track_point(self, element, way_point)

    def _create_schema_loc_str(self, xsi_schema_location: list[str]) -> str:
        """
        Create schema location string to write in GPX file.

        Parameters
        ----------
        xsi_schema_location : list[str]
            List of schema locations.

        Returns
        -------
        str
            Schema location string to write in GPX file.
        """
        schema_location_string = ""
        for loc in xsi_schema_location:
            schema_location_string += loc
            schema_location_string += " "
        schema_location_string = schema_location_string[:-1]
        return schema_location_string

    def add_root_properties(self) -> None:
        """
        Add properties to the GPX root element.
        """
        self.setIfNotNone(self.gpx_root, "version", self.gpx.version)
        self.setIfNotNone(self.gpx_root, "creator", "ezGPX")
        for k, v in self.gpx.xmlns.items():
            self.setIfNotNone(self.gpx_root, "xmlns:" +
                              k if k != "" else "xmlns", v)
        schema_location_string = self._create_schema_loc_str(
            self.gpx.xsi_schema_location)
        self.setIfNotNone(self.gpx_root, "xsi:schemaLocation",
                          schema_location_string)

    def add_root_metadata(self) -> None:
        """
        Add metadata element to the GPX root element.
        """
        self.gpx_root = self.add_metadata(self.gpx_root, self.gpx.metadata)

    def add_root_way_points(self) -> None:
        """
        Add wpt elements to the GPX root element.
        """
        for way_point in self.gpx.wpt:
            self.gpx_root = self.add_way_point(self.gpx_root, way_point)

    def add_root_routes(self) -> None:
        """
        Add rte elements to the GPX root element.
        """
        for route in self.gpx.rte:
            self.gpx_root = self.add_route(self.gpx_root, route)

    def add_root_tracks(self) -> None:
        """
        Add trck elements to the GPX root element.
        """
        logging.info("Preparing tracks...")

        for track in self.gpx.trk:
            self.gpx_root = self.add_track(self.gpx_root, track)

    def add_root_extensions(self) -> None:
        """
        Add extensions element to the GPX root element.
        """
        if self.gpx.extensions is not None:
            self.gpx_root = self.add_extensions(
                self.gpx_root, self.gpx.extensions, self.extensions_fields.get("gpx"))

    def gpx_to_string(self) -> str:
        """
        Convert Gpx instance to a string (the content of a .gpx file).

        Returns:
            str: String corresponding to the Gpx instance.
        """
        if self.gpx is not None:
            # Reset string
            self.gpx_string = ""

            # Root
            self.gpx_root = ET.Element("gpx")

            # Properties
            if self.properties:
                self.add_root_properties()

            # Metadata
            if self.metadata_fields:
                self.add_root_metadata()

            # Way points
            if self.way_point_fields:
                self.add_root_way_points()

            # Routes
            if self.route_fields:
                self.add_root_routes()

            # Tracks
            if self.track_fields:
                self.add_root_tracks()

            # Extensions
            if self.extensions_fields.get("gpx"):
                self.add_root_extensions()

            # Convert data to string
            logging.info("Converting GPX to string...")
            self.gpx_string = ET.tostring(self.gpx_root, encoding="unicode")
            # self.gpx_string = ET.tostring(gpx_root, encoding="utf-8")

            logging.info("GPX successfully converted to string:\n%s",
                         self.gpx_string)

            return self.gpx_string

    def write_gpx(self):
        """
        Convert Gpx instance to string and write to file.
        """
        # Open/create GPX file
        try:
            f = open(self.file_path, "w", encoding="utf-8")
        except OSError:
            logging.exception("Could not open/read file: %s",
                              self.file_path)
            raise
        # Write GPX file
        with f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
            f.write(self.gpx_string)

    def write(
            self,
            file_path: str,
            properties: bool = True,
            bounds_fields: List[str] = None,
            copyright_fields: List[str] = None,
            email_fields: List[str] = None,
            extensions_fields: dict = None,
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
            xml_schema: bool = False,
            xml_extensions_schemas: bool = False) -> bool:
        """
        TO UPDATE
        Handle writing.

        Args:
            path (str): Path to write the GPX file.
            properties (bool, optional): Toggle properties writting. Defaults to True.
            metadata (bool, optional): Toggle metadata writting. Defaults to True.
            way_point (bool, optional): Toggle way points writting. Defaults to True.
            routes (bool, optional): Toggle routes writting. Defaults to True.
            extensions (bool, optional): Toggle extensions writting. Defaults to True.
            ele (bool, optional): Toggle elevation writting. Defaults to True.
            time (bool, optional): Toggle time writting. Defaults to True.
            check_xml_schemas (bool, optional): Toggle schema verification after writting. Defaults to False.
            extensions_schemas (bool, optional): Toggle extensions schema verificaton after writing. Requires internet connection and is not guaranted to work. Defaults to False.

        Returns:
            bool: Return False if written file does not follow checked schemas. Return True otherwise.
        """
        directory_path = os.path.dirname(os.path.realpath(file_path))
        if not os.path.exists(directory_path):
            raise NotADirectoryError(
                errno.ENOENT, os.strerror(errno.ENOENT), directory_path)
        self.file_path = file_path
        self.file_name = os.path.basename(self.file_path)

        # Set parameters
        self.properties = properties
        self.bounds_fields = (bounds_fields
                              if bounds_fields is not None
                              else Bounds.fields)
        self.copyright_fields = (copyright_fields
                                 if copyright_fields is not None
                                 else Copyright.fields)
        self.email_fields = (email_fields
                             if email_fields is not None
                             else Email.fields)
        self.extensions_fields = (extensions_fields
                                  if extensions_fields is not None
                                  else {})
        self.gpx_fields = (gpx_fields
                           if gpx_fields is not None
                           else Gpx.fields)
        self.link_fields = (link_fields
                            if link_fields is not None
                            else Link.fields)
        self.metadata_fields = (metadata_fields
                                if metadata_fields is not None
                                else Metadata.fields)
        self.person_fields = (person_fields
                              if person_fields is not None
                              else Person.fields)
        self.point_segment_fields = (point_segment_fields
                                     if point_segment_fields is not None
                                     else PointSegment.fields)
        self.point_fields = (point_fields
                             if point_fields is not None
                             else Point.fields)
        self.route_fields = (route_fields
                             if route_fields is not None
                             else Route.fields)
        self.track_segment_fields = (track_segment_fields
                                     if track_segment_fields is not None
                                     else TrackSegment.fields)
        self.track_fields = (track_fields
                             if track_fields is not None
                             else Track.fields)
        self.way_point_fields = (way_point_fields
                                 if way_point_fields is not None
                                 else WayPoint.fields)
        self.track_point_fields = (track_point_fields
                                   if track_point_fields is not None
                                   else WayPoint.fields)

        # Check mandatory parameters
        def check_mandatory_fields(element, fields, mandatory_fields):
            if any(f not in fields for f in mandatory_fields):
                warnings.warn(f"{element} element must have following fields: {mandatory_fields}"
                            "Missing mandatory fields will automatically be added.")
                fields = list(set(fields + mandatory_fields))
            return fields
       
        self.bounds_fields = check_mandatory_fields("Bounds",
                                                    self.bounds_fields,
                                                    Bounds.mandatory_fields)
        self.copyright_fields = check_mandatory_fields("Copyright",
                                                       self.copyright_fields,
                                                       Copyright.mandatory_fields)
        self.email_fields = check_mandatory_fields("Email", self.email_fields,
                                                   Email.mandatory_fields)
        self.gpx_fields = check_mandatory_fields("Gpx", self.gpx_fields,
                                                 Gpx.mandatory_fields)
        self.link_fields = check_mandatory_fields("Link", self.link_fields,
                                                  Link.mandatory_fields)
        self.metadata_fields = check_mandatory_fields("Metadata",
                                                      self.metadata_fields,
                                                      Metadata.mandatory_fields)
        self.person_fields = check_mandatory_fields("Person",
                                                    self.person_fields,
                                                    Person.mandatory_fields)
        self.point_segment_fields = check_mandatory_fields("PointSegment",
                                                           self.point_segment_fields,
                                                           PointSegment.mandatory_fields)
        self.point_fields = check_mandatory_fields("Point", self.point_fields,
                                                   Point.mandatory_fields)
        self.route_fields = check_mandatory_fields("Route", self.route_fields,
                                                   Route.mandatory_fields)
        self.track_segment_fields = check_mandatory_fields("TrackSegment",
                                                           self.track_segment_fields,
                                                           TrackSegment.mandatory_fields)
        self.track_fields = check_mandatory_fields("Track", self.track_fields,
                                                   Track.mandatory_fields)
        self.way_point_fields = check_mandatory_fields("WayPoint",
                                                       self.way_point_fields,
                                                       WayPoint.mandatory_fields)
        self.track_point_fields = check_mandatory_fields("TrackPoint",
                                                         self.track_point_fields,
                                                         WayPoint.mandatory_fields)

        # Create methods behaviors
        self._add_bounds = self.behavior_creator.add_bounds_creator(
            self.bounds_fields)
        self._add_copyright = self.behavior_creator.add_copyright_creator(
            self.copyright_fields)
        self._add_email = self.behavior_creator.add_email_creator(
            self.email_fields)
        self._add_link = self.behavior_creator.add_link_creator(
            self.link_fields)
        self._add_metadata = self.behavior_creator.add_metadata_creator(
            self.metadata_fields)
        self._add_person = self.behavior_creator.add_person_creator(
            self.person_fields)
        self._add_point_segment = self.behavior_creator.add_point_segment_creator(
            self.point_segment_fields)
        self._add_point = self.behavior_creator.add_point_creator(
            self.point_fields)
        self._add_route = self.behavior_creator.add_route_creator(
            self.route_fields)
        self._add_track_segment = self.behavior_creator.add_track_segment_creator(
            self.track_segment_fields)
        self._add_track = self.behavior_creator.add_track_creator(
            self.track_fields)
        self._add_way_point = self.behavior_creator.add_way_point_creator(
            self.way_point_fields)
        self._add_track_point = self.behavior_creator.add_track_point_creator(
            self.track_point_fields)

        # Write .gpx file
        self.gpx_to_string()
        self.write_gpx()

        # Check XML schemas
        res = True
        if xml_schema or xml_extensions_schemas:
            res = self.check_xml_schemas(xml_schema, xml_extensions_schemas)

        return res
