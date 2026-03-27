"""
This module contains the XMLParser class.
"""

import warnings
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import IO

from dateutil import parser

from ..utils import check_xml_extensions_schemas, check_xml_schema
from .parser import Parser


class XMLParser(Parser):
    """
    XML file parser.
    """

    def __init__(
        self,
        source: str | Path | IO[str] | IO[bytes] | bytes,
        xml_schema: bool = True,
        xml_extensions_schemas: bool = False,
    ) -> None:
        """
        Initialise XML Parser instance.

        Args:
            source (str | Path | IO[str] | IO[bytes] | bytes): Path to
                a file or a file-like object to parse.
            xml_schema (bool, optional): Toggle  schema verification
                during parsing. Defaults to True.
            xml_extensions_schemas (bool, optional): Toggle extensions
                schema verificaton durign parsing. Requires internet
                connection and is not guaranted to work. Defaults to False.
        """
        self.name_spaces: dict = {
            node[0]: node[1] for _, node in ET.iterparse(source, events=["start-ns"])
        }
        self.extensions_fields: dict = {}

        super().__init__(source, self.name_spaces)

        self.xml_schema: bool = xml_schema
        self.xml_extensions_schemas: bool = xml_extensions_schemas

        self.xml_tree: ET.ElementTree = None
        self.xml_root: ET.Element = None

    def get_text(self, element: ET.Element, sub_element: str) -> str | None:
        """
        Get text from sub-element.

        Args:
            element (ET.Element): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            str | None: Text from sub-element.
        """
        text_ = element.get(sub_element)
        if text_ is None:
            warnings.warn(f"{element} has no attribute {sub_element}.")
        return text_

    def get_int(self, element: ET.Element, sub_element: str) -> int | None:
        """
        Get integer value from sub-element.

        Args:
            element (ET.Element): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            int | None: Integer value from sub-element.
        """
        int_ = element.get(sub_element)
        if int_ is None:
            warnings.warn(f"{element} has no attribute {sub_element}.")
        else:
            int_ = int(int_)
        return int_

    def get_float(self, element: ET.Element, sub_element: str) -> float | None:
        """
        Get floating point value from sub-element.

        Args:
            element (ET.Element): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            float | None: Floating point value from sub-element.
        """
        float_ = element.get(sub_element)
        if float_ is None:
            warnings.warn(f"{element} has no attribute {sub_element}.")
        else:
            float_ = float(float_)
        return float_

    def find_sub_element(
        self, element: ET.Element, sub_element: str
    ) -> ET.Element | None:
        """
        Find sub-element.

        Args:
            element (ET.Element): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            ET.Element | None: Sub-element.
        """
        sub_element_ = element.find(sub_element, self.name_spaces)
        if sub_element_ is None:
            warnings.warn(f"{element} has no attribute {sub_element}.")
        return sub_element_

    def find_text(self, element: ET.Element, sub_element: str) -> str | None:
        """
        Find text from sub-element.

        Args:
            element (ET.Element): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            str | None: Text from sub-element.
        """
        sub_element_ = self.find_sub_element(element, sub_element)
        return None if sub_element_ is None else sub_element_.text

    def find_int(self, element: ET.Element, sub_element: str) -> int | None:
        """
        Find integer value from sub-element.

        Args:
            element (ET.Element): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            int | None: Integer value from sub-element.
        """
        sub_element_ = self.find_sub_element(element, sub_element)
        return None if sub_element_ is None else int(sub_element_.text)

    def find_float(self, element: ET.Element, sub_element: str) -> float | None:
        """
        Find float point value from sub-element.

        Args:
            element (ET.Element): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            float | None: Floating point value from sub-element.
        """
        sub_element_ = self.find_sub_element(element, sub_element)
        return None if sub_element_ is None else float(sub_element_.text)

    def find_time(self, element: ET.Element, sub_element: str) -> datetime | None:
        """
        Find time value from sub-element.

        Args:
            element (ET.Element): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            datetime | None: Floating point value from sub-element.
        """
        sub_element_ = self.find_sub_element(element, sub_element)
        return None if sub_element_ is None else parser.parse(sub_element_.text)

    def xml_schemas(self):
        """
        Check XML schemas during parsing.
        """
        # Check XML schema
        if self.xml_schema:
            if not check_xml_schema(self.source, self.gpx.version):
                raise ValueError("Invalid GPX file (does not follow XML schema).")

        # Check XML extension schemas
        if self.xml_extensions_schemas:
            if not check_xml_extensions_schemas(self.source):
                raise ValueError(
                    "Invalid GPX file (does not follow XML extensions schemas)."
                )
