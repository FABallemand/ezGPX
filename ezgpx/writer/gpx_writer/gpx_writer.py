import os
import errno
import warnings
from typing import List, Dict
import logging
import xml.etree.ElementTree as ET

from ..writer import Writer
from ...gpx_elements import Bounds, Copyright, Email, Extensions, Gpx, Link, Metadata, Person, PointSegment, Point, Route, TrackSegment, Track, WayPoint
from .gpx_writer_method_behavior_creator import GPXWriterMethodBehaviorCreator

class GPXWriter(Writer):
    """
    GPX file writer.
    """

    def __init__(
            self,
            gpx: Gpx = None,
            file_path: str = None,
            precisions: Dict = None,
            time_format: str = None,
            extensions_fields: Dict = None) -> None:
        """
        Initialize GPXWriter instance.

        Args:
            gpx (Gpx, optional): Gpx instance to write. Defaults to None.
            file_path (str, optional): Path to the file to write. Defaults to None.
            precisions (dict, optional): Decimal precision for each type of value. Defaults to None.
            time_format (dict, optional): Time format. Defaults to None.
        """
        super().__init__(gpx, file_path)

        # Methods behavior creator
        self.behavior_creator: GPXWriterMethodBehaviorCreator = GPXWriterMethodBehaviorCreator()

        # Methods behaviors
        def placeholder_behavior(element, subelement):
            return None
        self._add_bounds = placeholder_behavior
        self._add_copyright = placeholder_behavior
        self._add_email = placeholder_behavior
        self._add_link = placeholder_behavior
        self._add_metadata = placeholder_behavior
        self._add_person = placeholder_behavior
        self._add_point_segment = placeholder_behavior
        self._add_point = placeholder_behavior
        self._add_route = placeholder_behavior
        self._add_track_segment = placeholder_behavior
        self._add_track = placeholder_behavior
        self._add_way_point = placeholder_behavior

        self._add_gpx_extensions = placeholder_behavior
        self._add_metadata_extensions = placeholder_behavior
        self._add_wpt_extensions = placeholder_behavior
        self._add_rte_extensions = placeholder_behavior
        self._add_trk_extensions = placeholder_behavior
        self._add_trkseg_extensions = placeholder_behavior

        # Parameters
        self.precisions: Dict = precisions
        self.time_format: str = time_format
        self.extensions_fields: Dict = extensions_fields

        # Utility attributes
        self.gpx_string: str = ""
        self.gpx_root = None
    
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
    
    def add_copyright(self, element: ET.Element, copyright: Copyright) -> ET.Element:
        """
        Add Copyright instance element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            copyright (Copyright): Copyright instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_copyright(self, element, copyright)
    
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
    
    def add_gpx_extensions(self, element: ET.Element, extensions: Extensions) -> ET.Element:
        """
        Add Extensions instance element to gpx GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            extensions (Extensions): Extensions instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_gpx_extensions(self, element, extensions)
    
    def add_metadata_extensions(self, element: ET.Element, extensions: Extensions) -> ET.Element:
        """
        Add Extensions instance element to metadata GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            extensions (Extensions): Extensions instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_metadata_extensions(self, element, extensions)
    
    def add_wpt_extensions(self, element: ET.Element, extensions: Extensions) -> ET.Element:
        """
        Add Extensions instance element to wpt GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            extensions (Extensions): Extensions instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_wpt_extensions(self, element, extensions)
    
    def add_rte_extensions(self, element: ET.Element, extensions: Extensions) -> ET.Element:
        """
        Add Extensions instance element to rte GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            extensions (Extensions): Extensions instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_rte_extensions(self, element, extensions)
    
    def add_trk_extensions(self, element: ET.Element, extensions: Extensions) -> ET.Element:
        """
        Add Extensions instance element to trk GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            extensions (Extensions): Extensions instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_trk_extensions(self, element, extensions)
    
    def add_trkseg_extensions(self, element: ET.Element, extensions: Extensions) -> ET.Element:
        """
        Add Extensions instance element to trkseg GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            extensions (Extensions): Extensions instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_trkseg_extensions(self, element, extensions)

    def createSchemaLocationString(self, xsi_schema_location: list[str]):
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
         
    def add_properties_garmin(self) -> None:
        """
        Add Garmin style properties to the GPX root element.
        """
        self.setIfNotNone(self.gpx_root, "xmlns", self.gpx.xmlns)
        self.setIfNotNone(self.gpx_root, "creator", self.gpx.creator)
        self.setIfNotNone(self.gpx_root, "version", self.gpx.version)
        schema_location_string = self.createSchemaLocationString(self.gpx.xsi_schema_location)
        self.setIfNotNone(self.gpx_root, "xsi:schemaLocation", schema_location_string)
        self.setIfNotNone(self.gpx_root, "xmlns:xsi", self.gpx.xmlns_xsi)
    
    def add_properties_strava(self) -> None:
        """
        Add Strava style properties to the GPX root element.
        """
        self.setIfNotNone(self.gpx_root, "creator", self.gpx.creator)
        self.setIfNotNone(self.gpx_root, "xmlns:xsi", self.gpx.xmlns_xsi)
        schema_location_string = self.createSchemaLocationString(self.gpx.xsi_schema_location)
        self.setIfNotNone(self.gpx_root, "xsi:schemaLocation", schema_location_string)
        self.setIfNotNone(self.gpx_root, "version", self.gpx.version)
        self.setIfNotNone(self.gpx_root, "xmlns", self.gpx.xmlns)
    
    def add_root_properties(self) -> None:
        """
        Add properties to the GPX root element.
        """
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
            self.gpx_root = self.add_extensions(self.gpx_root, self.gpx.extensions)

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

            logging.info(f"GPX successfully converted to string:\n{self.gpx_string}")

            return self.gpx_string

    def write_gpx(self):
        """
        Convert Gpx instance to string and write to file.
        """
        # Open/create GPX file
        try:
            f = open(self.file_path, "w")
        except OSError:
            logging.exception(f"Could not open/read file: {self.file_path}")
            raise
        # Write GPX file
        with f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
            f.write(self.gpx_string)

    def write(
            self,
            file_path: str,
            properties: bool = True,
            bounds_fields: List[str] = Bounds.fields,
            copyright_fields: List[str] = Copyright.fields,
            email_fields: List[str] = Email.fields,
            extensions_fields: dict = Extensions.fields,
            gpx_fields: List[str] = Gpx.fields,
            link_fields: List[str] = Link.fields,
            metadata_fields: List[str] = Metadata.fields,
            person_fields: List[str] = Person.fields,
            point_segment_fields: List[str] = PointSegment.fields,
            point_fields: List[str] = Point.fields,
            route_fields: List[str] = Route.fields,
            track_segment_fields: List[str] = TrackSegment.fields,
            track_fields: List[str] = Track.fields,
            way_point_fields: List[str] = WayPoint.fields,
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
            raise NotADirectoryError(errno.ENOENT, os.strerror(errno.ENOENT), directory_path)
        self.file_path = file_path
        self.file_name = os.path.basename(self.file_path)

        # Save parameters
        self.properties = properties # Change to List[str]? Combine with gpx_fields?
        self.bound_fields = bounds_fields
        self.copyright_fields = copyright_fields
        self.email_fields = email_fields
        self.extensions_fields_ = extensions_fields # TODO later, ability to personalise fields
        self.gpx_fields = gpx_fields
        self.link_fields = link_fields
        self.metadata_fields = metadata_fields
        self.person_fields = person_fields
        self.point_segment_fields = point_segment_fields
        self.point_fields = point_fields
        self.route_fields = route_fields
        self.track_segment_fields = track_segment_fields
        self.track_fields = track_fields
        self.way_point_fields = way_point_fields

        # Correct parameters
        if "lat" not in self.point_fields:
            warnings.warn("Point element must have 'lat' and 'lon' fields."
                          "Missing mandatory fields will automatically be added.")
            self.point_fields.append("lat")
        if "lon" not in self.point_fields:
            warnings.warn("Point element must have 'lat' and 'lon' fields."
                          "Missing mandatory fields will automatically be added.")
            self.point_fields.append("lon")
        if "lat" not in self.way_point_fields:
            warnings.warn("WayPoint element must have 'lat' and 'lon' fields."
                          "Missing mandatory fields will automatically be added.")
            self.way_point_fields.append("lat")
        if "lon" not in self.way_point_fields:
            warnings.warn("WayPoint element must have 'lat' and 'lon' fields."
                          "Missing mandatory fields will automatically be added.")
            self.way_point_fields.append("lon")

        # Create methods behaviors
        self._add_bounds = self.behavior_creator.add_bounds_creator(self.bound_fields)
        self._add_copyright = self.behavior_creator.add_copyright_creator(self.copyright_fields)
        self._add_email = self.behavior_creator.add_email_creator(self.email_fields)
        self._add_link = self.behavior_creator.add_link_creator(self.link_fields)
        self._add_metadata = self.behavior_creator.add_metadata_creator(self.metadata_fields)
        self._add_person = self.behavior_creator.add_person_creator(self.person_fields)
        self._add_point_segment = self.behavior_creator.add_point_segment_creator(self.point_segment_fields)
        self._add_point = self.behavior_creator.add_point_creator(self.point_fields)
        self._add_route = self.behavior_creator.add_route_creator(self.route_fields)
        self._add_track_segment = self.behavior_creator.add_track_segment_creator(self.track_segment_fields)
        self._add_track = self.behavior_creator.add_track_creator(self.track_fields)
        self._add_way_point = self.behavior_creator.add_way_point_creator(self.way_point_fields)

        self._add_gpx_extensions = self.behavior_creator.add_extensions_creator(self.extensions_fields.get("gpx"))
        self._add_metadata_extensions = self.behavior_creator.add_extensions_creator(self.extensions_fields.get("metadata"))
        self._add_wpt_extensions = self.behavior_creator.add_extensions_creator(self.extensions_fields.get("wpt"))
        self._add_rte_extensions = self.behavior_creator.add_extensions_creator(self.extensions_fields.get("rte"))
        self._add_trk_extensions = self.behavior_creator.add_extensions_creator(self.extensions_fields.get("trk"))
        self._add_trkseg_extensions = self.behavior_creator.add_extensions_creator(self.extensions_fields.get("trkseg"))

        # Write .gpx file
        self.gpx_to_string()
        self.write_gpx()

        # Check XML schemas
        res = True
        if xml_schema or xml_extensions_schemas:
            res = self.check_xml_schemas(xml_schema, xml_extensions_schemas)
            
        return res