import warnings
from typing import Dict, Optional, Union
import logging
from datetime import datetime
import xml.etree.ElementTree as ET

from .parser import Parser


class XMLParser(Parser):
    """
    XML File parser.
    """

    def __init__(
            self,
            file_path: Optional[str] = None,
            xml_schema: bool = True,
            xml_extensions_schemas: bool = False) -> None:
        """
        Initialize XML Parser instance.

        Parameters
        ----------
        file_path : Optional[str], optional
            Path to the file to parse, by default None
        xml_schema : bool, optional
            Toggle  schema verification during parsing, by default True
        xml_extensions_schemas : bool, optional
            Toggle extensions schema verificaton durign parsing.
            Requires internet connection and is not guaranted to work,
            by default False
        """
        self.name_spaces: dict = dict(
            [node for _, node in ET.iterparse(file_path, events=["start-ns"])])
        self.extensions_fields: Dict = {}

        super().__init__(file_path, self.name_spaces)

        self.xml_schema: bool = xml_schema
        self.xml_extensions_schemas: bool = xml_extensions_schemas

        self.xml_tree: ET.ElementTree = None
        self.xml_root: ET.Element = None

    def get_text(self, element, sub_element: str) -> Union[str, None]:
        """
        Get text from sub-element.

        Args:
            element (xml.etree.ElementTree.Element): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            Union[str, None]: Text from sub-element.
        """
        try:
            text_ = element.get(sub_element)
        except:
            logging.debug("%s has no attribute %s.", element, sub_element)
            text_ = None
        return text_

    def get_int(self, element, sub_element: str) -> Union[int, None]:
        """
        Get integer value from sub-element.

        Args:
            element (xml.etree.ElementTree.Element): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            Union[int, None]: Integer value from sub-element.
        """
        try:
            int_ = int(element.get(sub_element))
        except:
            logging.debug(f"{element} has no attribute {sub_element}.")
            int_ = None
        return int_

    def get_float(self, element, sub_element: str) -> Union[float, None]:
        """
        Get floating point value from sub-element.

        Args:
            element (xml.etree.ElementTree.Element): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            Union[float, None]: Floating point value from sub-element.
        """
        try:
            float_ = float(element.get(sub_element))
        except:
            logging.debug(f"{element} has no attribute {sub_element}.")
            float_ = None
        return float_

    def find_text(self, element, sub_element: str) -> Union[str, None]:
        """
        Find text from sub-element.

        Args:
            element (xml.etree.ElementTree.Element): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            Union[str, None]: Text from sub-element.
        """
        try:
            text_ = element.find(sub_element, self.name_spaces).text
        except:
            text_ = None
            logging.debug(f"{element} has no attribute {sub_element}.")
        return text_

    def find_int(self, element, sub_element: str) -> Union[int, None]:
        """
        Find integer value from sub-element.

        Args:
            element (xml.etree.ElementTree.Element): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            Union[int, None]: Integer value from sub-element.
        """
        try:
            int_ = int(element.find(sub_element, self.name_spaces).text)
        except:
            int_ = None
            logging.debug(f"{element} has no attribute {sub_element}.")
        return int_

    def find_float(self, element, sub_element: str) -> Union[float, None]:
        """
        Find float point value from sub-element.

        Args:
            element (xml.etree.ElementTree.Element): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            Union[float, None]: Floating point value from sub-element.
        """
        try:
            float_ = float(element.find(sub_element, self.name_spaces).text)
        except:
            float_ = None
            logging.debug(f"{element} has no attribute {sub_element}.")
        return float_

    def find_time(self, element, sub_element: str) -> Union[datetime, None]:
        """
        Find time value from sub-element.

        Args:
            element (xml.etree.ElementTree.Element): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            Union[datetime, None]: Floating point value from sub-element.
        """
        try:
            time_ = datetime.strptime(element.find(
                sub_element, self.name_spaces).text, self.time_format)
        except:
            time_ = None
            logging.debug(f"{element} has no attribute {sub_element}.")
        return time_

    def check_xml_schemas(self):
        """
        Check XML schemas during parsing.
        """
        # Check XML schema
        if self.xml_schema:
            if not self.gpx.check_xml_schema(self.file_path):
                raise ValueError("Invalid GPX file (does not follow XML schema).")

        # Check XML extension schemas
        if self.xml_extensions_schemas:
            if not self.gpx.check_xml_extensions_schemas(self.file_path):
                raise ValueError("Invalid GPX file (does not follow XML extensions schemas).")
