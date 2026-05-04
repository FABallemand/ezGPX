"""
This module contains the GPXWriter class.
"""

import errno
import os
import warnings
import xml.etree.ElementTree as ET
from typing import Optional

from ..complex_types import (
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
from .gpx_writer_method_creator import GPXWriterMethodCreator
from .writer import Writer


class GPXWriter(Writer):
    """
    GPX file writer.
    """

    def __init__(
        self, gpx: Gpx = None, precisions: dict = None, time_format: str = None
    ) -> None:
        """
        Initialise GPXWriter instance.

        Args:
            gpx (Gpx, optional): Gpx instance to write. Defaults to None.
            precisions (dict, optional): Decimal precision for each type of value. Defaults to None.
            time_format (str, optional): Time format. Defaults to None.
        """
        super().__init__(gpx, precisions, time_format)

        # Utility attributes
        self.gpx_string: str = ""
        self.gpx_root = None

        # Methods behavior creator
        self.behavior_creator: GPXWriterMethodCreator = GPXWriterMethodCreator()

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
        self._add_waypoint = self.placeholder_behavior
        self._add_track_point = self.placeholder_behavior

        # Fields
        self.properties: bool = None
        self.bounds_fields: list[str] = None
        self.copyright_fields: list[str] = None
        self.email_fields: list[str] = None
        self.extensions_fields: dict = None
        self.gpx_fields: list[str] = None
        self.link_fields: list[str] = None
        self.metadata_fields: list[str] = None
        self.person_fields: list[str] = None
        self.point_segment_fields: list[str] = None
        self.point_fields: list[str] = None
        self.route_fields: list[str] = None
        self.track_segment_fields: list[str] = None
        self.track_fields: list[str] = None
        self.waypoint_fields: list[str] = None
        self.track_point_fields: list[str] = None

    def placeholder_behavior(self, element, subelement):
        """
        Placeholder function for adding subelement to element in XML
        tree.
        """

    def add_bounds(self, element: ET.Element, bounds: Bounds) -> ET.Element:
        """
        Add Bounds instance to GPX element.

        Args:
            element (ET.Element): GPX element.
            bounds (Bounds): Bounds instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_bounds(self, element, bounds)

    def add_copyright(self, element: ET.Element, copyright_: Copyright) -> ET.Element:
        """
        Add Copyright instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            copyright (Copyright): Copyright instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_copyright(self, element, copyright_)

    def add_email(self, element: ET.Element, email: Email) -> ET.Element:
        """
        Add Email instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
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
                                self.set_not_none(extensions_, k1, v1)

                        # Add (n+1)-th level extensions
                        sub_extensions_ = self._add_extensions_rec(
                            sub_extensions_, v0["elmts"], extensions_fields[k0]["elmts"]
                        )
                    # Else, k0 contains a value
                    else:
                        extensions_, sub_extensions_ = self.add_subelement(
                            extensions_, k0, v0["elmts"]
                        )

                        # Set attributes
                        for k1, v1 in v0["attrib"].items():
                            if k1 in extensions_fields[k0]["attrib"].keys():
                                self.set_not_none(sub_extensions_, k1, v1)
        return extensions_

    def add_extensions(
        self, element: ET.Element, extensions: Extensions, extensions_fields: dict
    ) -> ET.Element:
        """
        Add Extensions instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            extensions (Extensions): Extensions instance to add.
            extensions_fields (dict): Extensions fields to add.

        Returns:
            ET.Element: GPX element.
        """
        if extensions is not None:
            extensions_ = ET.SubElement(element, extensions.tag)
            extensions_ = self._add_extensions_rec(
                extensions_, extensions.values, extensions_fields
            )
        return element

    def add_link(self, element: ET.Element, link: Link) -> ET.Element:
        """
        Add Link instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            link (Link): Link instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_link(self, element, link)

    def add_metadata(self, element: ET.Element, metadata: Metadata) -> ET.Element:
        """
        Add Metadata instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            metadata (Metadata): Metadata instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_metadata(self, element, metadata)

    def add_person(self, element: ET.Element, person: Person) -> ET.Element:
        """
        Add Person instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            person (Person): Person instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_person(self, element, person)

    def add_point_segment(
        self, element: ET.Element, point_segment: Ptseg
    ) -> ET.Element:
        """
        Add Ptseg instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            point_segment (Ptseg): Ptseg instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_point_segment(self, element, point_segment)

    def add_point(self, element: ET.Element, point: Pt) -> ET.Element:
        """
        Add Point instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            point (Point): Point instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_point(self, element, point)

    def add_route(self, element: ET.Element, route: Rte) -> ET.Element:
        """
        Add Rte instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            route (Rte): Rte instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_route(self, element, route)

    def add_track_segment(
        self, element: ET.Element, track_segment: Trkseg
    ) -> ET.Element:
        """
        Add Trkseg instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            track_segment (Trkseg): Trkseg instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_track_segment(self, element, track_segment)

    def add_track(self, element: ET.Element, track: Trk) -> ET.Element:
        """
        Add Trk instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            track (Trk): Trk instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_track(self, element, track)

    def add_waypoint(self, element: ET.Element, waypoint: Wpt) -> ET.Element:
        """
        Add Wpt instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            waypoint (Wpt): Wpt instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_waypoint(self, element, waypoint)

    def add_track_point(self, element: ET.Element, waypoint: Wpt) -> ET.Element:
        """
        Add Wpt instance (with trkpt tag) element to GPX element.

        Args:
            element (ET.Element): GPX element.
            waypoint (Wpt): Wpt instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_track_point(self, element, waypoint)

    def _create_schema_loc_str(self, xsi_schema_location: list[str]) -> str:
        """
        Create schema location string to write in GPX file.

        Args:
            xsi_schema_location (list[str]): List of schema locations.

        Returns:
            str: Schema location string to write in GPX file.
        """
        schema_location_string = ""
        for loc in xsi_schema_location:
            schema_location_string += loc
            schema_location_string += " "
        schema_location_string = schema_location_string[:-1]
        return schema_location_string

    def add_root_properties(self) -> None:
        """
        Add properties to the GPX root element and register name spaces.
        """
        self.set_not_none(self.gpx_root, "version", self.gpx.version)
        self.set_not_none(self.gpx_root, "creator", "ezGPX")
        for k, v in self.xmlns.items():
            ET.register_namespace(k, v)  # prefix, URI
            if k in ["", "xsi"]:
                self.set_not_none(
                    self.gpx_root, f"xmlns:{k}" if k != "" else "xmlns", v
                )
        self.set_not_none(
            self.gpx_root,
            "xsi:schemaLocation",
            self._create_schema_loc_str(self.gpx.xsi_schema_location),
        )

    def add_root_metadata(self) -> None:
        """
        Add metadata element to the GPX root element.
        """
        self.gpx_root = self.add_metadata(self.gpx_root, self.gpx.metadata)

    def add_root_waypoints(self) -> None:
        """
        Add wpt elements to the GPX root element.
        """
        for waypoint in self.gpx.wpt:
            self.gpx_root = self.add_waypoint(self.gpx_root, waypoint)

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
        for track in self.gpx.trk:
            self.gpx_root = self.add_track(self.gpx_root, track)

    def add_root_extensions(self) -> None:
        """
        Add extensions element to the GPX root element.
        """
        if self.gpx.extensions is not None:
            self.gpx_root = self.add_extensions(
                self.gpx_root, self.gpx.extensions, self.extensions_fields.get("gpx")
            )

    def gpx_to_string(self) -> str | None:
        """
        Convert Gpx instance to a string (the content of a .gpx file).

        Returns:
            str | None: String corresponding to the Gpx instance.
        """
        if self.gpx is None:
            return None

        # Reset string
        self.gpx_string = ""

        # Root
        self.gpx_root = ET.Element("gpx")

        # Properties
        self.add_root_properties()

        # Metadata
        if self.metadata_fields:
            self.add_root_metadata()

        # Way points
        if self.waypoint_fields:
            self.add_root_waypoints()

        # Rtes
        if self.route_fields:
            self.add_root_routes()

        # Trks
        if self.track_fields:
            self.add_root_tracks()

        # Extensions
        if self.extensions_fields.get("gpx"):
            self.add_root_extensions()

        # Convert data to string
        self.gpx_string = ET.tostring(self.gpx_root, encoding="unicode")
        # self.gpx_string = ET.tostring(gpx_root, encoding="utf-8")

        return self.gpx_string

    def write(
        self,
        file_path: str,
        *,
        xmlns: dict,
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
        xml_schema: bool = False,
        xml_extensions_schemas: bool = False,
    ) -> bool:
        """
        TODO update
        Handle writing.

        Args:
            path (str): Path to write the GPX file.
            xmlns (dict): TODO
            metadata (bool, optional): Toggle metadata writting. Defaults to True.
            waypoint (bool, optional): Toggle way points writting. Defaults to True.
            routes (bool, optional): Toggle routes writting. Defaults to True.
            extensions (bool, optional): Toggle extensions writting. Defaults to True.
            ele (bool, optional): Toggle elevation writting. Defaults to True.
            time (bool, optional): Toggle time writting. Defaults to True.
            xml_schemas (bool, optional): Toggle schema verification
                after writting. Defaults to False.
            extensions_schemas (bool, optional): Toggle extensions
                schema verificaton after writing. Requires internet
                connection and is not guaranted to work. Defaults to
                False.

        Returns:
            bool: Return False if written file does not follow checked
                schemas. Return True otherwise.
        """
        directory_path = os.path.dirname(os.path.realpath(file_path))
        if not os.path.exists(directory_path):
            raise NotADirectoryError(
                errno.ENOENT, os.strerror(errno.ENOENT), directory_path
            )
        self.file_path = file_path
        self.xmlns = xmlns

        # Set parameters
        self.bounds_fields = (
            bounds_fields if bounds_fields is not None else Bounds._fields
        )
        self.copyright_fields = (
            copyright_fields if copyright_fields is not None else Copyright._fields
        )
        self.email_fields = email_fields if email_fields is not None else Email._fields
        self.extensions_fields = (
            extensions_fields if extensions_fields is not None else {}
        )
        self.gpx_fields = gpx_fields if gpx_fields is not None else Gpx._fields
        self.link_fields = link_fields if link_fields is not None else Link._fields
        self.metadata_fields = (
            metadata_fields if metadata_fields is not None else Metadata._fields
        )
        self.person_fields = (
            person_fields if person_fields is not None else Person._fields
        )
        self.point_segment_fields = (
            point_segment_fields if point_segment_fields is not None else Ptseg._fields
        )
        self.point_fields = point_fields if point_fields is not None else Pt._fields
        self.route_fields = route_fields if route_fields is not None else Rte._fields
        self.track_segment_fields = (
            track_segment_fields if track_segment_fields is not None else Trkseg._fields
        )
        self.track_fields = track_fields if track_fields is not None else Trk._fields
        self.waypoint_fields = (
            waypoint_fields if waypoint_fields is not None else Wpt._fields
        )
        self.track_point_fields = (
            track_point_fields if track_point_fields is not None else Wpt._fields
        )

        # Check mandatory fields
        if mandatory_fields:

            def check_mandatory_fields(element, fields, mandatory_fields):
                if any(f not in fields for f in mandatory_fields):
                    warnings.warn(
                        f"{element} element must have following fields: {mandatory_fields}"
                        "Missing mandatory fields will automatically be added."
                    )
                    fields = set(fields + mandatory_fields)
                return fields

            self.bounds_fields = check_mandatory_fields(
                "Bounds", self.bounds_fields, Bounds._mandatory_fields
            )
            self.copyright_fields = check_mandatory_fields(
                "Copyright", self.copyright_fields, Copyright._mandatory_fields
            )
            self.email_fields = check_mandatory_fields(
                "Email", self.email_fields, Email._mandatory_fields
            )
            self.gpx_fields = check_mandatory_fields(
                "Gpx", self.gpx_fields, Gpx._mandatory_fields
            )
            self.link_fields = check_mandatory_fields(
                "Link", self.link_fields, Link._mandatory_fields
            )
            self.metadata_fields = check_mandatory_fields(
                "Metadata", self.metadata_fields, Metadata._mandatory_fields
            )
            self.person_fields = check_mandatory_fields(
                "Person", self.person_fields, Person._mandatory_fields
            )
            self.point_segment_fields = check_mandatory_fields(
                "Ptseg", self.point_segment_fields, Ptseg._mandatory_fields
            )
            self.point_fields = check_mandatory_fields(
                "Pt", self.point_fields, Pt._mandatory_fields
            )
            self.route_fields = check_mandatory_fields(
                "Rte", self.route_fields, Rte._mandatory_fields
            )
            self.track_segment_fields = check_mandatory_fields(
                "Trkseg", self.track_segment_fields, Trkseg._mandatory_fields
            )
            self.track_fields = check_mandatory_fields(
                "Trk", self.track_fields, Trk._mandatory_fields
            )
            self.waypoint_fields = check_mandatory_fields(
                "Wpt", self.waypoint_fields, Wpt._mandatory_fields
            )
            self.track_point_fields = check_mandatory_fields(
                "Trkpt", self.track_point_fields, Wpt._mandatory_fields
            )

        # Create methods behaviors
        self._add_bounds = self.behavior_creator.add_bounds_creator(self.bounds_fields)
        self._add_copyright = self.behavior_creator.add_copyright_creator(
            self.copyright_fields
        )
        self._add_email = self.behavior_creator.add_email_creator(self.email_fields)
        self._add_link = self.behavior_creator.add_link_creator(self.link_fields)
        self._add_metadata = self.behavior_creator.add_metadata_creator(
            self.metadata_fields
        )
        self._add_person = self.behavior_creator.add_person_creator(self.person_fields)
        self._add_point_segment = self.behavior_creator.add_point_segment_creator(
            self.point_segment_fields
        )
        self._add_point = self.behavior_creator.add_point_creator(self.point_fields)
        self._add_route = self.behavior_creator.add_route_creator(self.route_fields)
        self._add_track_segment = self.behavior_creator.add_track_segment_creator(
            self.track_segment_fields
        )
        self._add_track = self.behavior_creator.add_track_creator(self.track_fields)
        self._add_waypoint = self.behavior_creator.add_waypoint_creator(
            self.waypoint_fields
        )
        self._add_track_point = self.behavior_creator.add_track_point_creator(
            self.track_point_fields
        )

        # Write .gpx file
        self.gpx_to_string()
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>' + self.gpx_string)

        # Check XML schemas
        res = True
        if xml_schema or xml_extensions_schemas:
            res = self.xml_schemas(xml_schema, xml_extensions_schemas)

        return res
