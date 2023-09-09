import os
from typing import Optional, Union, List, Tuple, Dict
import logging
import xml.etree.ElementTree as ET
import xmlschema
from datetime import datetime

from ..writer import Writer
from ..gpx_elements import Gpx

DEFAULT_NORMAL_STYLE = {"color": "ff0000ff",
                "width": 2,
                "fill": 0
                }

DEFAULT_HIGHLIGHT_STYLE = {"color": "ff0000ff",
                   "width": 2,
                   "fill": 0
                   }

DEFAULT_STYLES = [("normal", DEFAULT_NORMAL_STYLE),
                  ("highlight", DEFAULT_HIGHLIGHT_STYLE)
                  ]

class KMLWriter(Writer):
    """
    KML file writer.
    """

    def __init__(
            self,
            gpx: Gpx = None,
            path: str = None,
            properties: bool = True,
            metadata: bool = True, # unused
            way_points: bool = True,
            routes: bool = True,
            extensions: bool = True,
            ele: bool = True,
            time: bool = True,
            precisions: Dict = None,
            time_format: str = None,
            styles: List[Tuple[str, Dict]] = DEFAULT_STYLES) -> None:
        """
        Initialize GPXWriter instance.
        """
        super().__init__(gpx, path)
        self.file_name: str = ""
        self.kml_string: str = ""

        # Parameters
        self.properties: bool = properties
        self.metadata: bool = metadata
        self.way_points: bool = way_points
        self.routes: bool = routes
        self.extensions: bool = extensions
        self.ele: bool = ele
        self.time: bool = time

        self.precisions: Dict = precisions
        self.time_format = time_format

        self.styles = styles

        self.kml_root = None
    
    def add_pair(self, element: ET.Element, key: str, style_url: str) -> ET.Element:
        """
        Add StyleMap to KML element.

        Parameters
        ----------
        element : ET.Element
            KML element.
        key : str
            Key.
        style_url : str
            Style URL.

        Returns
        -------
        ET.Element
            KML element.
        """
        pair_ = ET.SubElement(element, "Pair")
        pair_, _ = self.add_subelement(pair_, "key", key)
        pair_, _ = self.add_subelement(pair_, "styleUrl", style_url)
        return element
    
    def add_stylemap(self, element: ET.Element, id: str) -> ET.Element:
        """
        Add StyleMap to KML element.

        Parameters
        ----------
        element : ET.Element
            KML element.
        id : str
            StyleMap element id.

        Returns
        -------
        ET.Element
            KML element.
        """
        stylemap_ = ET.SubElement(element, "StyleMap")
        stylemap_.set("id", id)
        style_id = 1
        for style_key, style in self.styles:
            stylemap_ = self.add_pair(stylemap_, style_key, "#style" + str(style_id))
            style_id += 1
        return element
    
    def add_polystyle(self, element: ET.Element, style: Dict) -> ET.Element:
        """
        Add PolyStyle to KML element.

        Parameters
        ----------
        element : ET.Element
            KML element.
        style : Dict
            Style.

        Returns
        -------
        ET.Element
            KML element.
        """
        polystyle_ = ET.SubElement(element, "PolyStyle")
        try:
            polystyle_, _ = self.add_subelement_number(polystyle_, "fill", style["fill"])
        except:
            logging.warning("No fill attribute in style")
            polystyle_, _ = self.add_subelement_number(polystyle_, "fill", 0)
        return element
    
    def add_linestyle(self, element: ET.Element, style: Dict) -> ET.Element:
        """
        Add LineStyle to KML element.

        Parameters
        ----------
        element : ET.Element
            KML element.
        style : Dict
            Style.

        Returns
        -------
        ET.Element
            KML element.
        """
        linestyle_ = ET.SubElement(element, "LineStyle")
        try:
            linestyle_, _ = self.add_subelement(linestyle_, "color", style["color"])
        except:
            logging.warning("No color attribute in style")
            linestyle_, _ = self.add_subelement(linestyle_, "color", "ff0000ff")
        try:
            linestyle_, _ = self.add_subelement_number(linestyle_, "width", style["width"])
        except:
            logging.warning("No width attribute in style")
            linestyle_, _ = self.add_subelement_number(linestyle_, "width", 2)
        return element
    
    def add_style(self, element: ET.Element, id: str, style: Dict) -> ET.Element:
        """
        Add Style to KML element.

        Parameters
        ----------
        element : ET.Element
            KML element.
        id : str
            Style element id.
        style : Dict
            Line style.

        Returns
        -------
        ET.Element
            KML element.
        """
        style_ = ET.SubElement(element, "Style")
        style_.set("id", id)
        style_ = self.add_linestyle(style_, style)
        style_ = self.add_polystyle(style_, style)
        return element
    
    def add_linestring(self, element: ET.Element) -> ET.Element:
        """
        Add LineString to KML element.

        Parameters
        ----------
        element : ET.Element
            KML element.

        Returns
        -------
        ET.Element
            KML element.
        """
        linestring_ = ET.SubElement(element, "LineString")
        linestring_, _ = self.add_subelement_number(linestring_, "tessellate", 1)
        coordinates = self.gpx.to_csv(path=None, columns=["lon", "lat", "ele"], header=False).replace("\n", " ")
        linestring_, _ = self.add_subelement(linestring_, "coordinates", coordinates)
        return element
    
    def add_placemark(self, element: ET.Element) -> ET.Element:
        """
        Add Placemark to KML element.

        Parameters
        ----------
        element : ET.Element
            KML element.

        Returns
        -------
        ET.Element
            KML element.
        """
        placemark_ = ET.SubElement(element, "Placemark")
        placemark_, _ = self.add_subelement(placemark_, "name", self.gpx.name())
        placemark_, _ = self.add_subelement(placemark_, "styleUrl", "#stylemap")
        placemark_ = self.add_linestring(placemark_)
        return element

    def add_document(self, element: ET.Element) -> ET.Element:
        """
        Add Document to KML element.

        Parameters
        ----------
        element : ET.Element
            KML element.

        Returns
        -------
        ET.Element
            KML element.
        """
        document_ = ET.SubElement(element, "Document")
        document_, _ = self.add_subelement(document_, "name", self.file_name)
        id = 1
        for style_key, style in self.styles:
            document_ = self.add_style(document_, "style" + str(id), style)
            id += 1
        document_ = self.add_stylemap(document_, "stylemap")
        document_ = self.add_placemark(document_)
        return element

    def add_root_document(self) -> None:
        """
        Add Document element to the KML root element.
        """
        logging.info("Preparing Document...")

        self.kml_root = self.add_document(self.kml_root)
    
    def add_root_properties(self) -> None:
        """
        Add properties to the GPX root element.
        """
        logging.info("Preparing properties...")

        # According to .kml file from Google Earth Pro
        self.kml_root.set("xmlns", "http://www.opengis.net/kml/2.2")
        self.kml_root.set("xmlns:gx", "http://www.google.com/kml/ext/2.2")
        self.kml_root.set("xmlns:kml", "http://www.opengis.net/kml/2.2")
        self.kml_root.set("xmlns:atom", "http://www.w3.org/2005/Atom")

    def gpx_to_string(self) -> str:
        """
        Convert Gpx instance to a string (the content of a .kml file).

        Returns:
            str: String corresponding to the Gpx instance.
        """
        if self.gpx is not None:
            logging.info("Start convertion from GPX to string")
            # Reset string
            self.kml_string = ""

            # Root
            self.kml_root = ET.Element("kml")

            # Properties
            if self.properties:
                self.add_root_properties()

            # Document
            self.add_root_document()

            # Convert data to string
            logging.info("Converting GPX to string...")
            self.gpx_string = ET.tostring(self.kml_root, encoding="unicode")
            # self.gpx_string = ET.tostring(kml_root, encoding="utf-8")

            logging.info(f"GPX successfully converted to string:\n{self.gpx_string}")

            return self.gpx_string

    def write_gpx(self):
        """
        Convert Gpx instance to string and write to file.
        """
        # Open/create GPX file
        try:
            f = open(self.path, "w")
        except OSError:
            logging.exception(f"Could not open/read file: {self.path}")
            raise
        # Write GPX file
        with f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
            f.write(self.gpx_string)

    def write(
            self,
            path: str,
            styles: Optional[List[Tuple[str, Dict]]] = None,
            check_schemas: bool = False) -> bool:
        """
        Handle writing.

        Parameters
        ----------
        path : str
            Path to write the KML file.
        styles : Optional[List[Tuple[str, Dict]]], optional
            List of (style_id, style) tuples, by default None
        check_schemas : bool, optional
            Toggle schema verification after writting, by default False

        Returns
        -------
        bool
            bool: Return False if written file does not follow checked schemas. Return True otherwise.
        """
        # Handle path
        directory_path = os.path.dirname(os.path.realpath(path))
        if not os.path.exists(directory_path):
            logging.error("Provided path does not exist")
            return
        self.path = path
        self.file_name = os.path.basename(self.path)
        
        # Update style
        if styles is not None:
            self.styles = styles
        
        # Write .kml file
        self.gpx_to_string()
        self.write_gpx()

        # Check schema
        if check_schemas:
            # Load schema
            current_file_path = os.path.dirname(os.path.abspath(__file__))
            schema = xmlschema.XMLSchema(os.path.join(current_file_path, "../schemas/kml_2_2/ogckml22.xsd"))
            
            # Check schema
            if schema is not None:
                return schema.is_valid(self.path)
            else:
                logging.error("Unable to check XML schema")
                return True
        return True