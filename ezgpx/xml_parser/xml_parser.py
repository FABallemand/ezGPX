from typing import Optional, Union
import logging
from datetime import datetime
import xml.etree.ElementTree as ET

from ..parser import Parser

class XMLParser(Parser):
    """
    XML File parser.
    """

    def __init__(self, file_path: Optional[str] = None, name_space: Optional[dict] = None, check_schemas: bool = True, extensions_schemas: bool = False) -> None:
        """
        Initialize Parser instance.

        Args:
            file_path (str, optional): Path to the file to parse. Defaults to None.
            name_space (dict, optional): File XML name spaces.
            check_schemas (bool, optional): Toggle schema verification during parsing. Defaults to True.
            extensions_schemas (bool, optional): Toggle extensions schema verificaton durign parsing. Requires internet connection and is not guaranted to work. Defaults to False.
        """
        super().__init__(file_path)
        
        self.name_space: dict = None
        if name_space is None:
            self.name_space = {}
        else:
            self.name_space = name_space

        self.check_schemas: bool = check_schemas
        self.extensions_schemas: bool = extensions_schemas

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
            logging.debug(f"{element} has no attribute {sub_element}.")
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
            text_ = element.find(sub_element, self.name_space).text
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
            int_ = int(element.find(sub_element, self.name_space).text)
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
            float_ = float(element.find(sub_element, self.name_space).text)
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
            time_ = datetime.strptime(element.find(sub_element, self.name_space).text, self.time_format)
        except:
            time_ = None
            logging.debug(f"{element} has no attribute {sub_element}.")
        return time_