import os
from typing import Optional, Union, List, Dict
import logging
import xml.etree.ElementTree as ET

from .xml_parser import XMLParser
from ..gpx_elements import Gpx, TrackSegment, Track, WayPoint


class KMLParser(XMLParser):
    """
    KML file parser.
    """

    def __init__(
            self,
            file_path: Optional[str] = None,
            check_xml_schemas: bool = True,
            xml_extensions_schemas: bool = False) -> None:
        """
        Initialize KMLParser instance.

        Args:
            file_path (str, optional): Path to the file to parse. Defaults to None.
            check_xml_schemas (bool, optional): Toggle schema verification during parsing. Defaults to True.
            xml_extensions_schemas (bool, optional): Toggle extensions schema verificaton durign parsing. Requires internet connection and is not guaranted to work. Defaults to False.
        """
        if not file_path.endswith(".kml"):
            return
        super().__init__(file_path, check_xml_schemas, xml_extensions_schemas)

        if self.file_path is not None and os.path.exists(self.file_path):
            self.parse()
        else:
            logging.warning("File path does not exist")

    def find_precisions(self):
        """
        Find decimal precision of any type of value in a KML file (latitude, elevation...).
        """
        # Point
        documents = self.xml_root.findall("opengis:Document", self.name_spaces)
        placemarks = documents[0].findall(
            "opengis:Placemark", self.name_spaces)
        linestrings = placemarks[0].findall(
            "opengis:LineString", self.name_spaces)
        coordinates = self.find_text(linestrings[0], "opengis:coordinates")

        coordinates = coordinates.replace("\n", "").replace("\t", "")
        if coordinates[-1] == " ":
            coordinates = coordinates[:-1]
        coordinates = coordinates.split(" ")
        coordinates = coordinates[0].split(",")

        self.precisions["lat_lon"] = self.find_precision(coordinates[0])
        self.precisions["elevation"] = self.find_precision(coordinates[2])

    # def parse_linestring(self, linestring) -> List[str]:
    #     """
    #     Parse LineString element from KML file.

    #     Args:
    #         placemark (xml.etree.ElementTree.Element): Parsed LineString element.

    #     Returns:
    #         List[str]: Informations contained in the LineString element (strings of coordinates).
    #     """
    #     if linestring is None:
    #         return None

    #     linestrings_data = []
    #     coordinatess = linestring.findall("opengis:coordinates", self.name_space)
    #     for coordinates in coordinatess:
    #         linestrings_data.append(coordinates.text)

    #     return linestrings_data

    def parse_placemark(self, placemark) -> Union[Dict, None]:
        """
        Parse Placemark element from KML file.

        Args:
            placemark (xml.etree.ElementTree.Element): Parsed Placemark element.

        Returns:
            Union[List[Dict], None]: Informations contained in the Placemark element (the name of the Placemark (str) and the contents of the LineString (List[str])).
        """
        if placemark is None:
            return None

        placemark_data = {}

        placemark_data["name"] = self.find_text(placemark, "opengis:name")

        placemark_data["linestrings_data"] = []
        linestrings = placemark.findall("opengis:LineString", self.name_spaces)
        for linestring in linestrings:
            placemark_data["linestrings_data"].append(
                self.find_text(linestring, "opengis:coordinates"))

        return placemark_data

    def parse_document(self, document) -> Union[List[Dict], None]:
        """
        Parse Document element from KML file.

        Args:
            document (xml.etree.ElementTree.Element): Parsed Document element.

        Returns:
            Union[List[Dict], None]: Informations related to Placemark elements contained in
            the Document element.
        """
        if document is None:
            return None

        # name = self.find_text(document, "opengis:name")

        placemmarks_data = []
        placemarks = document.findall("opengis:Placemark", self.name_spaces)
        for placemark in placemarks:
            placemmarks_data.append(self.parse_placemark(placemark))

        return placemmarks_data

    def parse_root_document(self):
        """
        Parse Document elements from KML file.
        """
        documents = self.xml_root.findall("opengis:Document", self.name_spaces)
        for document in documents:
            placemarks_data = self.parse_document(document)

            if len(placemarks_data) == 1:
                placemark_data = placemarks_data[0]
                linestrings_data = placemark_data["linestrings_data"]
                trkseg = []
                for coordinates in linestrings_data:
                    coordinates = coordinates.replace(
                        "\n", "").replace("\t", "")
                    if coordinates[-1] == " ":
                        coordinates = coordinates[:-1]
                    coordinates = coordinates.split(" ")
                    trkpt = []
                    for point_coord in coordinates:
                        point_coord = point_coord.split(",")
                        trkpt.append(WayPoint(tag="trkpt",
                                              lat=float(point_coord[1]),
                                              lon=float(point_coord[0]),
                                              ele=float(point_coord[2])))
                    trkseg.append(TrackSegment(trkpt=trkpt))

                tracks = [Track(name=placemark_data["name"], trkseg=trkseg)]
                self.gpx.trk = tracks
            else:
                logging.error("Oops, not yet implemented...")

    def add_properties(self):
        self.gpx.creator = "ezGPX"
        self.gpx.xmlns = "http://www.topografix.com/GPX/1/1"
        self.gpx.version = "1.1"
        self.gpx.xmlns_xsi = "http://www.w3.org/2001/XMLSchema-instance"
        self.gpx.xsi_schema_location = [
            "http://www.topografix.com/GPX/1/1", "http://www.topografix.com/GPX/1/1/gpx.xsd"]

    def parse(self) -> Gpx:
        """
        Parse KML file.

        Returns:
            Gpx: Gpx instance.
        """
        # Parse KML file
        try:
            self.xml_tree = ET.parse(self.file_path)
            self.xml_root = self.xml_tree.getroot()
        except Exception as err:
            logging.exception("Unexpected %s, %s.\n"
                              "Unable to parse KML file.", err, type(err))
            raise

        # Add properties
        self.add_properties()

        # Find precisions
        self.find_precisions()

        # Check XML schemas
        self.check_xml_schemas()

        # Parse Document
        try:
            self.parse_root_document()
        except:
            logging.error("Unable to parse tracks in GPX file.")
            raise

        logging.debug("Parsing complete!!")
        return self.gpx
