import logging
import xml.etree.ElementTree as ET

from ..gpx_elements import Bounds, Copyright, Email, Extensions, Gpx, Link, Metadata, Person, TrackPoint, TrackSegment, Track


class Writer():
    """
    GPX file writer.
    """

    def __init__(
            self,
            gpx: Gpx = None,
            path: str = "",
            metadata: bool = True,
            ele: bool = True,
            time: bool = True,
            lat_lon_precision: int = 7,
            ele_precision: int = 1) -> None:
        self.gpx = gpx
        self.path = path
        self.gpx_string = ""

        # Parameters
        self.metadata = metadata
        self.ele = ele
        self.time = time

        self.lat_lon_precision = lat_lon_precision
        self.ele_precision = ele_precision

    def add_subelement(self, element, sub_element, text: str = None):
        """
        Add sub-element to GPX element.

        Args:
            element (xml.etree.ElementTree.Element): GPX element.
            sub_element (str): GPX sub-element.
            text (str): GPX sub-element text. Defaults to None.

        Returns:
            xml.etree.ElementTree.Element: GPX element.
            xml.etree.ElementTree.Element: GPX sub-element.
        """
        if text is not None:
            sub_elmnt = ET.SubElement(element, sub_element)
            sub_elmnt.text = text
        return element, sub_elmnt
    
    def add_bounds(self, element: ET.Element, bounds: Bounds) -> ET.Element:
        element, bounds = self.add_subelement(element, "bounds")
        bounds, _ = self.add_subelement(bounds, "minlat", "{:.{}f}".format(bounds.minlat, self.lat_lon_precision))
        bounds, _ = self.add_subelement(bounds, "minlon", "{:.{}f}".format(bounds.minlon, self.lat_lon_precision))
        bounds, _ = self.add_subelement(bounds, "maxlat", "{:.{}f}".format(bounds.maxlat, self.lat_lon_precision))
        bounds, _ = self.add_subelement(bounds, "maxlon", "{:.{}f}".format(bounds.maxlon, self.lat_lon_precision))
        return element
    
    def add_copyright(self, element: ET.Element, copyright: Copyright) -> ET.Element:
        element, copyright = self.add_subelement(element, "copyright")
        copyright.set("author", copyright.author)
        copyright, _ = self.add_subelement(copyright, "year", str(copyright.year))
        copyright, _ = self.add_subelement(copyright, "licence", str(copyright.licence))

    ## DO OTHER add_* functions

    def metadata_to_string(self, gpx_root: ET.Element) -> ET.Element:
        
        logging.debug("Converting metadata to string...")

        metadata = ET.SubElement(gpx_root, "metadata")

        metadata = self.add_subelement(metadata, "name", self.gpx.metadata.name)
        metadata = self.add_subelement(metadata, "desc", self.gpx.metadata.desc)

        if self.gpx.metadata.author is not None:
            author = ET.SubElement(metadata, "author")
            author = self.add_subelement(author, "name", self.gpx.metadata.author.name)
            # Add email and link

        if self.gpx.metadata.copyright is not None:
            # Add copyright
            pass

        if self.gpx.metadata.link is not None:
            # Add link
            pass

        metadata = self.add_subelement(metadata, "time", self.gpx.metadata.time.strftime("%Y-%m-%dT%H:%M:%SZ"))
        metadata = self.add_subelement(metadata, "keywords", self.gpx.metadata.keywords)

        if self.gpx.metadata.bounds is not None:
            metadata = self.add_bounds(metadata, self.gpx.metadata.bounds)

        if self.gpx.metadata.extensions is not None:
            # Add extensions
            pass

        return gpx_root
    
    def tracks_to_string(self, gpx_root: ET.Element) -> ET.Element:

        logging.debug("Converting tracks to string...")

        for gpx_track in self.gpx.tracks:
            track = ET.SubElement(gpx_root, "trk")
            track = self.add_subelement(track, "name", gpx_track.name)

            # Track segments
            for gpx_segment in gpx_track.trkseg:
                segment = ET.SubElement(track, "trkseg")

                # Track points
                for gpx_point in gpx_segment.trkpt:
                    point = ET.SubElement(segment, "trkpt")
                    point.set("lat", "{:.{}f}".format(gpx_point.latitude, self.lat_lon_precision))
                    point.set("lon", "{:.{}f}".format(gpx_point.longitude, self.lat_lon_precision))
                    if self.ele:
                        ele = ET.SubElement(point, "ele")
                        ele.text = "{:.{}f}".format(gpx_point.elevation, self.ele_precision)
                    if self.time:
                        time = ET.SubElement(point, "time")
                        time.text = gpx_point.time.strftime("%Y-%m-%dT%H:%M:%SZ")

    def gpx_to_string(self, gpx: Gpx = None, metadata: bool = True, ele: bool = True, time: bool = True) -> str:

        if gpx is not None:
            self.gpx = gpx

        # Is it smart ??
        self.metadata = metadata
        self.ele = ele
        self.time = time

        if self.gpx is not None:
            logging.debug("Start convertion from GPX to string")
            # Reset string
            self.gpx_string = ""

            # Root
            gpx_root = ET.Element("gpx")

            # Metadata
            if self.metadata:
                gpx_root = self.metadata_to_string(gpx_root, self.gpx.metadata)

            # Tracks
            gpx_root = self.tracks_to_string(gpx_root)

            # Convert data to string
            self.gpx_string = ET.tostring(gpx_root)

            logging.debug(f"GPX successfully converted to string\n{self.gpx_string}")

            return self.gpx_string

    def write_gpx(self, path: str = ""):

        if path != "":
            self.path = path

        if self.path != "":
            # Write GPX file
            with open(self.path, "wb") as f:
                f.write(b"<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
                f.write(self.gpx_string)

    def write(self, gpx: Gpx = None, path: str = "", metadata: bool = True, ele: bool = True, time: bool = True):
        
        if gpx is not None:
            self.gpx = gpx

        if path != "":
            self.path = path

        if self.gpx is not None:
            self.gpx_to_string()

        # Is it smart ??
        self.metadata = metadata
        self.ele = ele
        self.time = time

        if self.path != "": # + Check if path is correct
            self.write_gpx()

