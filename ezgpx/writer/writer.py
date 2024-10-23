from typing import Union, Tuple
import logging
import xml.etree.ElementTree as ET
from datetime import datetime

from ..gpx_elements import Gpx
from ..parser import DEFAULT_PRECISION, DEFAULT_TIME_FORMAT


class Writer():
    """
    File writer.
    """

    def __init__(
            self,
            gpx: Gpx = None,
            file_path: str = None) -> None:
        """
        Initialize Writer instance.

        Parameters
        ----------
        gpx : Gpx, optional
            Gpx instance to write, by default None
        file_path : str, optional
            Path to the file to write, by default None
        """
        self.gpx: Gpx = gpx
        self.file_path: str = file_path

    def setIfNotNone(self, element: ET.Element, field: str, value):
        """
        _summary_

        Parameters
        ----------
        element : ET.Element
            _description_
        field : str
            _description_
        value : _type_
            _description_
        """
        if value is not None:
            element.set(field, value)

    def add_subelement(
            self, element: ET.Element, sub_element: str,
            text: str) -> Tuple[ET.Element, Union[ET.Element, None]]:
        """
        Add sub-element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            sub_element (str): GPX sub-element.
            text (str): GPX sub-element text.

        Returns:
            Tuple[xml.etree.ElementTree.Element, Union[xml.etree.ElementTree.Element, None]]: GPX element and GPX sub-element (if not None).
        """
        sub_element_ = None
        if text is not None:
            sub_element_ = ET.SubElement(element, sub_element)
            sub_element_.text = text
        return element, sub_element_

    def add_subelement_number(
            self, element: ET.Element, sub_element: str,
            number: Union[int, float],
            precision: int = DEFAULT_PRECISION) -> Tuple[ET.Element, Union[ET.Element, None]]:
        """
        Add sub-element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            sub_element (str): GPX sub-element.
            number (Union[int, float], optional): GPX sub-element value.
            precision (int, optional): Precision. Defaults to DEFAULT_PRECISION.

        Returns:
            Tuple[xml.etree.ElementTree.Element, Union[xml.etree.ElementTree.Element, None]]: GPX element and GPX sub-element (if not None).
        """
        sub_element_ = None
        if number is not None:
            sub_element_ = ET.SubElement(element, sub_element)
            if isinstance(number, int):
                sub_element_.text = str(number)
            elif isinstance(number, float):
                sub_element_.text = f"{number:.{precision}f}"
            else:
                logging.error("Invalid number type.")
        return element, sub_element_

    def add_subelement_time(
            self, element: ET.Element, sub_element: str, time: datetime,
            format_: str = DEFAULT_TIME_FORMAT) -> ET.Element:
        """
        Add sub-element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            sub_element (str): GPX sub-element.
            time (datetime, optional): GPX sub-element value.
            format (str, optional): Format. Defaults to DEFAULT_TIME_FORMAT.

        Returns:
            Tuple[xml.etree.ElementTree.Element, Union[xml.etree.ElementTree.Element, None]]: GPX element and GPX sub-element (if not None).
        """
        sub_element_ = None
        if time is not None:
            sub_element_ = ET.SubElement(element, sub_element)
            try:
                sub_element_.text = time.strftime(format_)
            except:
                logging.error("Invalid time format.")
        return element, sub_element_

    def check_xml_schemas(
            self,
            xml_schema: bool = False,
            xml_extensions_schemas: bool = False) -> bool:
        """
        Check XML schemas after writting.

        Parameters
        ----------
        xml_schema : bool, optional
            Toggle XML schema verification, by default False.
        xml_extensions_schemas : bool, optional
            Toggle XML extensions schemas verification, by default False.

        Returns
        -------
        bool
            True if the written file follows all verified schemas.
        """
        # Check XML schema
        if xml_schema:
            if not self.gpx.check_xml_schema(self.file_path):
                logging.error("Invalid GPX file (does not follow XML schema).")
                return False

        # Check XML extension schemas
        if xml_extensions_schemas:
            if not self.gpx.check_xml_extensions_schemas(self.file_path):
                logging.error(
                    "Invalid GPX file (does not follow XML extensions schemas).")
                return False

        return True
