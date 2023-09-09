import os
from typing import Optional, Union, Tuple
import logging
import xml.etree.ElementTree as ET
from datetime import datetime

from ..gpx_elements import Gpx
from ..gpx_parser import DEFAULT_PRECISION, DEFAULT_TIME_FORMAT

class Writer():
    """
    File writer.
    """

    def __init__(
            self,
            gpx: Gpx = None,
            path: str = None) -> None:
        """
        Initialize Writer instance.

        Parameters
        ----------
        gpx : Gpx, optional
            Gpx instance to write, by default None
        path : str, optional
            Path to the file to write, by default None
        """
        self.gpx: Gpx = gpx
        self.path: str = path

    def add_subelement(self, element: ET.Element, sub_element: str, text: str) -> Tuple[ET.Element, Union[ET.Element, None]]:
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
    
    def add_subelement_number(self, element: ET.Element, sub_element: str, number: Union[int, float], precision: int = DEFAULT_PRECISION) -> Tuple[ET.Element, Union[ET.Element, None]]:
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
            if type(number) is int:
                sub_element_.text = str(number)
            elif type(number) is float:
                sub_element_.text = "{:.{}f}".format(number, precision)
            else:
                logging.error("Invalid number type.")
        return element, sub_element_
    
    def add_subelement_time(self, element: ET.Element, sub_element: str, time: datetime, format: str = DEFAULT_TIME_FORMAT) -> ET.Element:
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
                sub_element_.text = time.strftime(format)
            except:
                logging.error("Invalid time format.")
        return element, sub_element_