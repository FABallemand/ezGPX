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
from .writer import GPXLike, Writer


class GPXWriter(Writer):
    """
    GPX file writer.
    """

    def __init__(self, gpx: GPXLike) -> None:
        """
        Initialise GPXWriter instance.

        Args:
            gpx (GPXLike): GPX instance to write.
        """
        super().__init__(gpx)

        # Utility attributes
        self.gpx_string: str = ""
        self.gpx_root = None

        # Methods behavior creator
        self.method_creator: GPXWriterMethodCreator = GPXWriterMethodCreator()

        # Methods behaviors
        self._add_bounds = self.placeholder_method
        self._add_copyright = self.placeholder_method
        self._add_email = self.placeholder_method
        self._add_link = self.placeholder_method
        self._add_metadata = self.placeholder_method
        self._add_person = self.placeholder_method
        self._add_ptseg = self.placeholder_method
        self._add_pt = self.placeholder_method
        self._add_rte = self.placeholder_method
        self._add_trkseg = self.placeholder_method
        self._add_trk = self.placeholder_method
        self._add_wpt = self.placeholder_method
        self._add_trkpt = self.placeholder_method

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
        self.ptseg_fields: list[str] = None
        self.pt_fields: list[str] = None
        self.rte_fields: list[str] = None
        self.trkseg_fields: list[str] = None
        self.trk_fields: list[str] = None
        self.wpt_fields: list[str] = None
        self.trkpt_fields: list[str] = None

    def placeholder_method(self, element, subelement):
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
        if extensions is not None and extensions.values is not None:
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

    def add_ptseg(self, element: ET.Element, pt_segment: Ptseg) -> ET.Element:
        """
        Add Ptseg instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            pt_segment (Ptseg): Ptseg instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_ptseg(self, element, pt_segment)

    def add_pt(self, element: ET.Element, pt: Pt) -> ET.Element:
        """
        Add Pt instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            pt (Pt): Pt instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_pt(self, element, pt)

    def add_rte(self, element: ET.Element, rte: Rte) -> ET.Element:
        """
        Add Rte instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            rte (Rte): Rte instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_rte(self, element, rte)

    def add_trkseg(self, element: ET.Element, trkseg: Trkseg) -> ET.Element:
        """
        Add Trkseg instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            trkseg (Trkseg): Trkseg instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_trkseg(self, element, trkseg)

    def add_trk(self, element: ET.Element, trk: Trk) -> ET.Element:
        """
        Add Trk instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            trk (Trk): Trk instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_trk(self, element, trk)

    def add_wpt(self, element: ET.Element, wpt: Wpt) -> ET.Element:
        """
        Add Wpt instance element to GPX element.

        Args:
            element (ET.Element): GPX element.
            wpt (Wpt): Wpt instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_wpt(self, element, wpt)

    def add_trkpt(self, element: ET.Element, wpt: Wpt) -> ET.Element:
        """
        Add Wpt instance (with trkpt tag) element to GPX element.

        Args:
            element (ET.Element): GPX element.
            wpt (Wpt): Wpt instance to add.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
        """
        return self._add_trkpt(self, element, wpt)

    def add_root_properties(self) -> None:
        """
        Add properties to the GPX root element and register name spaces.
        """
        self.set_not_none(self.gpx_root, "version", self.gpx.gpx.version)
        self.set_not_none(self.gpx_root, "creator", "ezGPX")
        for k, v in self.gpx.xmlns.items():
            ET.register_namespace(k, v)  # prefix, URI
            if k in ["", "xsi"]:
                self.set_not_none(
                    self.gpx_root, f"xmlns:{k}" if k != "" else "xmlns", v
                )
        self.set_not_none(
            self.gpx_root,
            "xsi:schemaLocation",
            " ".join(f"{k} {v}" for k, v in self.gpx.xsi_schema_location.items()),
        )

    def add_root_metadata(self) -> None:
        """
        Add metadata element to the GPX root element.
        """
        self.gpx_root = self.add_metadata(self.gpx_root, self.gpx.gpx.metadata)

    def add_root_wpts(self) -> None:
        """
        Add wpt elements to the GPX root element.
        """
        for wpt in self.gpx.gpx.wpt:
            self.gpx_root = self.add_wpt(self.gpx_root, wpt)

    def add_root_rtes(self) -> None:
        """
        Add rte elements to the GPX root element.
        """
        for rte in self.gpx.gpx.rte:
            self.gpx_root = self.add_rte(self.gpx_root, rte)

    def add_root_trks(self) -> None:
        """
        Add trck elements to the GPX root element.
        """
        for trk in self.gpx.gpx.trk:
            self.gpx_root = self.add_trk(self.gpx_root, trk)

    def add_root_extensions(self) -> None:
        """
        Add extensions element to the GPX root element.
        """
        if self.gpx.gpx.extensions is not None:
            self.gpx_root = self.add_extensions(
                self.gpx_root,
                self.gpx.gpx.extensions,
                self.extensions_fields.get("gpx"),
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
        if self.wpt_fields:
            self.add_root_wpts()

        # Rtes
        if self.rte_fields:
            self.add_root_rtes()

        # Trks
        if self.trk_fields:
            self.add_root_trks()

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
        bounds_fields: Optional[list[str]] = None,
        copyright_fields: Optional[list[str]] = None,
        email_fields: Optional[list[str]] = None,
        extensions_fields: Optional[dict] = None,
        gpx_fields: Optional[list[str]] = None,
        link_fields: Optional[list[str]] = None,
        metadata_fields: Optional[list[str]] = None,
        person_fields: Optional[list[str]] = None,
        ptseg_fields: Optional[list[str]] = None,
        pt_fields: Optional[list[str]] = None,
        rte_fields: Optional[list[str]] = None,
        trkseg_fields: Optional[list[str]] = None,
        trk_fields: Optional[list[str]] = None,
        wpt_fields: Optional[list[str]] = None,
        trkpt_fields: Optional[list[str]] = None,
        mandatory_fields: bool = True,
    ) -> None:
        """
        TODO
        """
        directory_path = os.path.dirname(os.path.realpath(file_path))
        if not os.path.exists(directory_path):
            raise NotADirectoryError(
                errno.ENOENT, os.strerror(errno.ENOENT), directory_path
            )
        self.file_path = file_path

        # Set parameters
        self.bounds_fields = Bounds._fields if bounds_fields is None else bounds_fields
        self.copyright_fields = (
            Copyright._fields if copyright_fields is None else copyright_fields
        )
        self.email_fields = Email._fields if email_fields is None else email_fields
        self.extensions_fields = {} if extensions_fields is None else extensions_fields
        self.gpx_fields = Gpx._fields if gpx_fields is None else gpx_fields
        self.link_fields = Link._fields if link_fields is None else link_fields
        self.metadata_fields = (
            Metadata._fields if metadata_fields is None else metadata_fields
        )
        self.person_fields = Person._fields if person_fields is None else person_fields
        self.ptseg_fields = Ptseg._fields if ptseg_fields is None else ptseg_fields
        self.pt_fields = Pt._fields if pt_fields is None else pt_fields
        self.rte_fields = Rte._fields if rte_fields is None else rte_fields
        self.trkseg_fields = Trkseg._fields if trkseg_fields is None else trkseg_fields
        self.trk_fields = Trk._fields if trk_fields is None else trk_fields
        self.wpt_fields = Wpt._fields if wpt_fields is None else wpt_fields
        self.trkpt_fields = Wpt._fields if trkpt_fields is None else trkpt_fields

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
            self.ptseg_fields = check_mandatory_fields(
                "Ptseg", self.ptseg_fields, Ptseg._mandatory_fields
            )
            self.pt_fields = check_mandatory_fields(
                "Pt", self.pt_fields, Pt._mandatory_fields
            )
            self.rte_fields = check_mandatory_fields(
                "Rte", self.rte_fields, Rte._mandatory_fields
            )
            self.trkseg_fields = check_mandatory_fields(
                "Trkseg", self.trkseg_fields, Trkseg._mandatory_fields
            )
            self.trk_fields = check_mandatory_fields(
                "Trk", self.trk_fields, Trk._mandatory_fields
            )
            self.wpt_fields = check_mandatory_fields(
                "Wpt", self.wpt_fields, Wpt._mandatory_fields
            )
            self.trkpt_fields = check_mandatory_fields(
                "Trkpt", self.trkpt_fields, Wpt._mandatory_fields
            )

        # Create methods behaviors
        self._add_bounds = self.method_creator.add_bounds_creator(self.bounds_fields)
        self._add_copyright = self.method_creator.add_copyright_creator(
            self.copyright_fields
        )
        self._add_email = self.method_creator.add_email_creator(self.email_fields)
        self._add_link = self.method_creator.add_link_creator(self.link_fields)
        self._add_metadata = self.method_creator.add_metadata_creator(
            self.metadata_fields
        )
        self._add_person = self.method_creator.add_person_creator(self.person_fields)
        self._add_ptseg = self.method_creator.add_ptseg_creator(self.ptseg_fields)
        self._add_pt = self.method_creator.add_pt_creator(self.pt_fields)
        self._add_rte = self.method_creator.add_rte_creator(self.rte_fields)
        self._add_trkseg = self.method_creator.add_trkseg_creator(self.trkseg_fields)
        self._add_trk = self.method_creator.add_trk_creator(self.trk_fields)
        self._add_wpt = self.method_creator.add_wpt_creator(self.wpt_fields)
        self._add_trkpt = self.method_creator.add_trkpt_creator(self.trkpt_fields)

        # Write .gpx file
        self.gpx_to_string()
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>' + self.gpx_string)
