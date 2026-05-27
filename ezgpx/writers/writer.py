"""
This module contains the Writer class.
"""

import warnings
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any, Protocol

from ..constants.precisions import (
    DEFAULT_PRECISION,
    DEFAULT_TIME_FORMAT,
)


class GPXLike(Protocol):
    """Protocol for GPX objects."""


class Writer:
    """
    File writer.
    """

    def __init__(self, gpx: GPXLike) -> None:
        """
        Initialise Writer instance.

        Args:
            gpx (GPXLike): GPX instance to write.
        """
        self.gpx: GPXLike = gpx
        self.precisions: dict = gpx._precisions
        self.time_format: str = gpx._time_format
        self.file_path: str = None

    def get_value(self, attribute: Any) -> Any | None:
        """
        Safely get attribute value.
        """
        try:
            return attribute.value
        except AttributeError:
            return None

    def set_not_none(self, element: ET.Element, field: str, value):
        """
        TODO

        Args:
            element (ET.Element): _description_
            field (str): _description_
            value (_type_): _description_
        """
        if value is not None:
            element.set(field, value)

    def add_subelement(
        self, element: ET.Element, sub_element: str, text: str
    ) -> tuple[ET.Element, ET.Element | None]:
        """
        Add sub-element to GPX element.

        Args:
            element (ET.Element): GPX element.
            sub_element (str): GPX sub-element.
            text (str): GPX sub-element text.

        Returns:
            tuple[ET.Element, ET.Element | None]: GPX element and
                GPX sub-element (if not None).
        """
        sub_element_ = None
        if text is not None:
            sub_element_ = ET.SubElement(element, sub_element)
            sub_element_.text = text
        return element, sub_element_

    def add_subelement_number(
        self,
        element: ET.Element,
        sub_element: str,
        number: int | float,
        precision: int = DEFAULT_PRECISION,
    ) -> tuple[ET.Element, ET.Element | None]:
        """
        Add sub-element to GPX element.

        Args:
            element (ET.Element): GPX element.
            sub_element (str): GPX sub-element.
            number (int | float, optional): GPX sub-element value.
            precision (int, optional): Precision. Defaults to DEFAULT_PRECISION.

        Returns:
            tuple[ET.Element, ET.Element | None]: GPX element and
                GPX sub-element (if not None).
        """
        sub_element_ = None
        if number is not None:
            sub_element_ = ET.SubElement(element, sub_element)
            if isinstance(number, int):
                sub_element_.text = str(number)
            elif isinstance(number, float):
                sub_element_.text = f"{number:.{precision}f}"
            else:
                warnings.warn("Invalid number type.")
        return element, sub_element_

    def add_subelement_time(
        self,
        element: ET.Element,
        sub_element: str,
        time: datetime,
        format_: str = DEFAULT_TIME_FORMAT,
    ) -> tuple[ET.Element, ET.Element | None]:
        """
        Add sub-element to GPX element.

        Args:
            element (ET.Element): GPX element.
            sub_element (str): GPX sub-element.
            time (datetime, optional): GPX sub-element value.
            format (str, optional): Format. Defaults to DEFAULT_TIME_FORMAT.

        Returns:
            tuple[ET.Element, ET.Element | None]: GPX element and
                GPX sub-element (if not None).
        """
        sub_element_ = None
        if time is not None:
            sub_element_ = ET.SubElement(element, sub_element)
            time_utc = time.astimezone(timezone.utc)  # Convert to UTC
            sub_element_.text = time_utc.strftime(format_)
        return element, sub_element_
