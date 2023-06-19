import logging
from datetime import datetime
import xml.etree.ElementTree as ET

from ..gpx_elements import Gpx, Metadata, Track

class Writer():

    def __init__(self, gpx: Gpx = None, path: str = "", metadata: bool = True, ele: bool = True, time: bool = True):
        
        self.gpx = gpx
        self.path = path
        self.gpx_string = ""

        # Parameters
        self.metadata = metadata
        self.ele = ele
        self.time = time

    def add_subelement(self, element, sub_element, text):
        """
        Add sub-element to GPX element.

        Args:
            element (???): GPX element.
            sub_element (str): GPX sub-element.
            text (str): GPX sub-element text.

        Returns:
            ???: GPX element.
        """
        if text is not None:
            sub_elmnt = ET.SubElement(element, sub_element)
            sub_elmnt.text = text
        return element

    def metadata_to_string(self, metadata: Metadata):
        pass

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
                logging.debug("Converting metadata to string...")

                # self.gpx_string += self.metadata_to_string(self.gpx.metadata)

                # metadata = ET.SubElement(gpx_root, "metadata")

                # metadata = self.add_subelement(metadata, "name", self.gpx.metadata.name)
                # metadata = self.add_subelement(metadata, "desc", self.gpx.metadata.desc)

                if self.gpx.metadata.author is not None:
                    pass
                    # author = ET.SubElement(metadata, "author")
                    # author = self.add_subelement(author, "name", self.gpx.metadata.author.name)
                    # Add email and link

                if self.gpx.metadata.copyright is not None:
                    # Add copyright
                    pass

                if self.gpx.metadata.link is not None:
                    # Add link
                    pass

                # metadata = self.add_subelement(metadata, "time", self.gpx.metadata.time)
                # metadata = self.add_subelement(metadata, "keywords", self.gpx.metadata.keywords)

                if self.gpx.metadata.bounds is not None:
                    # Add bounds
                    pass

                if self.gpx.metadata.extensions is not None:
                    # Add extensions
                    pass

            # Tracks
            logging.debug("Converting tracks to string...")

            for gpx_track in self.gpx.tracks:
                track = ET.SubElement(gpx_root, "trk")
                # name = ET.SubElement(track, "name")
                # name.text = gpx_track.name

                # Track segments
                for gpx_segment in gpx_track.trkseg:
                    segment = ET.SubElement(track, "trkseg")

                    # Track points
                    for gpx_point in gpx_segment.trkpt:
                        point = ET.SubElement(segment, "trkpt")
                        point.set("lat", str(gpx_point.latitude))
                        point.set("lon", str(gpx_point.longitude))
                        if self.ele:
                            ele = ET.SubElement(point, "ele")
                            ele.text = str(gpx_point.elevation)
                        if self.time:
                            time = ET.SubElement(point, "time")
                            time.text = gpx_point.time.strftime("%Y-%m-%dT%H:%M:%SZ")

            # Convert data to string
            self.gpx_string = ET.tostring(gpx_root)

            logging.debug("GPX successfully converted to string")

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

