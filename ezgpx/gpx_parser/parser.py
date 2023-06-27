from typing import Optional, Union
import logging
from datetime import datetime

import xml.etree.ElementTree as ET

from ..gpx_elements import Bounds, Copyright, Email, Extensions, Gpx, Link, Metadata, Person, TrackPoint, TrackSegment, Track

DEFAULT_PRECISION = 2

class Parser():
    """
    GPX file parser.
    """

    def __init__(self, file_path: str = ""):
        self.file_path: str = file_path
        self.gpx_tree: ET.ElementTree = None
        self.gpx_root: ET.Element = None
        self.name_space: dict = {"topo": "http://www.topografix.com/GPX/1/1"}
        self.precisions: dict = {"lat_lon": DEFAULT_PRECISION,
                                "elevation": DEFAULT_PRECISION,
                                "distance": DEFAULT_PRECISION,
                                "duration": DEFAULT_PRECISION,
                                "speed": DEFAULT_PRECISION,
                                "rate": DEFAULT_PRECISION}
        self.gpx: Gpx = Gpx()

        if self.file_path != "":
            self.parse()

    def check_schema(self):
        pass

    def find_precision(self, number: str) -> int:

        if number is None:
            return DEFAULT_PRECISION
        
        try:
            test = float(number)

            if "." in number:
                _, decimal = number.split(sep=".")
                return len(decimal)
            else:
                return 0
        except:
            logging.error(f"Unable to find precision of number: {number}")
            raise

    def find_precisions(self):
        # Point
        track = self.gpx_root.findall("topo:trk", self.name_space)[0]
        segment = track.findall("topo:trkseg", self.name_space)[0]
        point = segment.findall("topo:trkpt", self.name_space)[0]

        self.precisions["lat_lon"] = self.find_precision(point.get("lat"))
        self.precisions["elevation"] = self.find_precision(self.find_text(point, "topo:ele"))

        # Extensions
        extensions = segment.find("topo:extensions", self.name_space)

        if extensions is not None:
            self.precisions["distance"] = self.find_precision(self.find_text(extensions, "topo:Distance"))
            self.precisions["duration"] = self.find_precision(self.find_text(extensions, "topo:TotalElapsedTime"))
            self.precisions["speed"] = self.find_precision(self.find_text(extensions, "topo:MovingSpeed"))
            self.precisions["rate"] = self.find_precision(self.find_text(extensions, "topo:AvgAscentRate"))

    def get_text(self, element, sub_element: str) -> str:
        """
        Get text from sub-element.

        Args:
            element (???): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            str: Text from sub-element.
        """
        try:
            text = element.get(sub_element)
            logging.debug(f"{text} - {type(text)}")
        except:
            logging.debug(f"{element} has no attribute {sub_element}")
            text = None
        return text
    
    def find_text(self, element, sub_element: str) -> str:
        """
        Find text from sub-element.

        Args:
            element (???): Parsed element from GPX file.
            sub_element (str): Sub-element name.

        Returns:
            str: Text from sub-element.
        """
        try:
            text = element.find(sub_element, self.name_space).text
            # logging.debug(f"{text} - {type(text)}")
        except:
            text = None
            logging.debug(f"{element} has no attribute {sub_element}")
        return text
    
    def parse_properties(self):

        self.gpx.creator = self.gpx_root.attrib["creator"]
        self.gpx.version = self.gpx_root.attrib["version"]
        self.gpx.xmlns = self.gpx_root.tag[1:-4]
        name_spaces = self.gpx_root.get("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation").split(" ")
        self.gpx.xsi_schema_location = [x for x in name_spaces if x != ""]

    def parse_bounds(self, bounds) -> Bounds:
        """
        Parse bounds element in GPX file.

        Args:
            bounds (???): Parsed bounds element.

        Returns:
            Bounds: Bounds object.
        """
        if bounds is None:
            return None

        minlat = self.get_text(bounds, "minlat")
        minlon = self.get_text(bounds, "minlon")
        maxlat = self.get_text(bounds, "maxlat")
        maxlon = self.get_text(bounds, "maxlon")
        return Bounds(minlat, minlon, maxlat, maxlon)
    
    def parse_copyright(self, copyright) -> Copyright:
        """
        Parse copyright element in GPX file.

        Args:
            copyright (???): Parsed copyright element.

        Returns:
            Copyright: Copyright object.
        """
        if copyright is None:
            return None
        
        author = self.get_text(copyright, "author")
        year = self.find_text(copyright, "topo:year")
        licence = self.find_text(copyright, "topo:licence")
        return Copyright(author, year, licence)
    
    def parse_email(self, email) -> Email:
        """
        Parse email element in GPX file.

        Args:
            email (???): Parsed email element.

        Returns:
            Email: Email object.
        """
        if email is None:
            return None
        
        id = self.get_text(email, "id")
        domain = self.get_text(email, "domain")
        return Email(id, domain)
    
    def parse_extensions(self, extensions) -> Extensions:
        """
        Parse extensions element in GPX file.

        Args:
            extensions (???): Parsed extensions element.

        Returns:
            Extensions: Extensions object.
        """
        if extensions is None:
            return None
        
        display_color = self.find_text(extensions, "topo:DisplayColor")
        distance = self.find_text(extensions, "topo:Distance")
        total_elapsed_time = self.find_text(extensions, "topo:TotalElapsedTime")
        moving_time = self.find_text(extensions, "topo:MovingTime")
        stopped_time = self.find_text(extensions, "topo:StoppedTime")
        moving_speed = self.find_text(extensions, "topo:MovingSpeed")
        max_speed = self.find_text(extensions, "topo:MaxSpeed")
        max_elevation = self.find_text(extensions, "topo:MaxElevation")
        min_elevation = self.find_text(extensions, "topo:MinElevation")
        ascent = self.find_text(extensions, "topo:Ascent")
        descent = self.find_text(extensions, "topo:Descent")
        avg_ascent_rate = self.find_text(extensions, "topo:AvgAscentRate")
        max_ascent_rate = self.find_text(extensions, "topo:MaxAscentRate")
        avg_descent_rate = self.find_text(extensions, "topo:AvgDescentRate")
        max_descent_rate = self.find_text(extensions, "topo:MaxDescentRate")
        return Extensions(display_color, distance, total_elapsed_time, moving_time, stopped_time, moving_speed, max_speed, max_elevation, min_elevation, ascent, descent, avg_ascent_rate, max_ascent_rate, avg_descent_rate, max_descent_rate)

    def parse_link(self, link) -> Link:
        """
        Parse link element in GPX file.

        Args:
            link (???): Parsed link element.

        Returns:
            Link: Link object.
        """
        if link is None:
            return None
        
        href = self.get_text(link, "href")
        text = self.find_text(link, "topo:text")
        type = self.find_text(link, "topo:type")
        return Link(href, text, type)
    
    def parse_person(self, person) -> Person:
        """
        Parse person element in GPX file.

        Args:
            person (???): Parsed person element.

        Returns:
            Person: Person object.
        """
        if person is None:
            return None
        
        name = self.find_text(person, "topo:name")
        email = self.parse_email(person.find("topo:email", self.name_space))
        link = self.parse_link(person.find("topo:link", self.name_space))
        return Person(name, email, link)
    
    def parse_metadata(self):
        """
        Parse metadata element in GPX File.
        """
        
        metadata = self.gpx_root.find("topo:metadata", self.name_space)

        name = self.find_text(metadata, "topo:name")
        desc = self.find_text(metadata, "topo:desc")
        author = self.parse_person(metadata.find("topo:author", self.name_space))
        copyright = self.parse_copyright(metadata.find("topo:copyright", self.name_space))
        link = self.parse_link(metadata.find("topo:link", self.name_space))
        time = datetime.strptime(metadata.find("topo:time", self.name_space).text, "%Y-%m-%dT%H:%M:%SZ")
        keywords = self.find_text(metadata, "topo:keywords")
        bounds = self.parse_bounds(metadata.find("topo:bounds", self.name_space))
        extensions = self.parse_extensions(metadata.find("topo:extensions", self.name_space))

        self.gpx.metadata = Metadata(name, desc, author, copyright, link, time, keywords, bounds, extensions)

    def parse_point(self, point) -> TrackPoint:
        """
        Parse trkpt element from GPX file.

        Args:
            point (???): Parsed trkpt element.

        Returns:
            TrackPoint: TrackPoint object.
        """
        try:
            lat = float(point.get("lat"))
        except:
            logging.error(f"{point} contains invalid latitude: {point.get('lat')}")
            lat = None

        try:
            lon = float(float(point.get("lon")))
        except:
            logging.error(f"{point} contains invalid longitude: {float(point.get('lon'))}")
            lon = None
        
        try:
            elevation = float(self.find_text(point, "topo:ele"))
        except:
            logging.error(f"{point} contains invalid elevation: {self.find_text(point, 'topo:ele')}")
            elevation = None
        try:
            time = datetime.strptime(self.find_text(point, "topo:time"), "%Y-%m-%dT%H:%M:%SZ")
        except:
            logging.error(f"{point} contains invalid time: {self.find_text(point, 'topo:time')}")
            time = None

        return TrackPoint(lat, lon, elevation, time)

    def parse_segment(self, segment) -> TrackSegment:
        """
        Parse trkseg element from GPX file.

        Args:
            segment (???): Parsed trkseg element.

        Returns:
            TrackSegment: TrackSegment object.
        """
        # Points
        trkpt = []
        points = segment.findall("topo:trkpt", self.name_space)
        for point in points:
            trkpt.append(self.parse_point(point))

        # Extensions
        extensions = self.parse_extensions(segment.find("topo:extensions", self.name_space))

        return TrackSegment(trkpt, extensions)

    def parse_track(self, track) -> Track:
        """
        Parse trk element in GPX file.

        Args:
            track (???): Parsed trk element.

        Returns:
            Track: Track object.
        """
        name = self.find_text(track, "topo:name")
        cmt = self.find_text(track, "topo:cmt")
        desc = self.find_text(track, "topo:desc")
        src = self.find_text(track, "topo:src")
        link = self.parse_link(track.find("topo:link", self.name_space))
        try:
            number = int(self.find_text(track, "topo:number"))
        except:
            logging.error(f"{track} contains invalid number: {self.find_text(track, 'topo:number')}")
            number = None
        type = self.find_text(track, "topo:type")
        extensions = self.parse_extensions(track.find("topo:extensions", self.name_space))

        trkseg = []
        segments = track.findall("topo:trkseg", self.name_space)
        for segment in segments:
            trkseg.append(self.parse_segment(segment))

        return Track(name, cmt, desc, src, link, number, type, extensions, trkseg)

    def parse_tracks(self):
        """
        Parse track elements in GPX file.
        """
        # Tracks
        tracks = self.gpx_root.findall("topo:trk", self.name_space)
        for track in tracks:
            self.gpx.tracks.append(self.parse_track(track))

    def parse(self, file_path: str = "") -> Gpx:
        """
        Parse GPX file.

        Args:
            file_path (str, optional): Path to the file to parse. Defaults to "".

        Returns:
            Gpx: Gpx object., self.name_space).text
        """
        # File
        if file_path != "":
            self.file_path = file_path
        elif self.file_path == "":
            logging.error("No GPX file to parse")
            return

        # Parse GPX file
        try:
            self.gpx_tree = ET.parse(self.file_path)
            self.gpx_root = self.gpx_tree.getroot()
        except:
            logging.exception("Unable to parse GPX file")
            raise

        # Parse properties
        try:
            self.parse_properties()
        except:
            logging.exception("Unable to parse properties in GPX file")
            raise
        
        # Parse metadata
        try:
            self.parse_metadata()
        except:
            logging.exception("Unable to parse metadata in GPX file")
            raise

        # Parse tracks
        try:
            self.parse_tracks()
        except:
            logging.exception("Unable to parse tracks in GPX file")
            raise

        # Find precision
        self.find_precisions()

        logging.debug("Parsing complete")
        return self.gpx