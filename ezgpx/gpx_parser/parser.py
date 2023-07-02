from typing import Optional, Union
import logging
from datetime import datetime
import xml.etree.ElementTree as ET

from ..gpx_elements import Bounds, Copyright, Email, Extensions, Gpx, Link, Metadata, Person, Route, TrackPoint, TrackSegment, Track, WayPoint

DEFAULT_PRECISION = 2

class Parser():
    """
    GPX file parser.
    """

    def __init__(self, file_path: str = "") -> None:
        """
        initialize Parser instance.

        Args:
            file_path (str, optional): Path to the file to parse. Defaults to "".
        """
        self.file_path: str = file_path

        self.gpx_tree: ET.ElementTree = None
        self.gpx_root: ET.Element = None

        self.name_space: dict = {"topo": "http://www.topografix.com/GPX/1/1"}
        self.precisions: dict = {
            "lat_lon": DEFAULT_PRECISION,
            "elevation": DEFAULT_PRECISION,
            "distance": DEFAULT_PRECISION,
            "duration": DEFAULT_PRECISION,
            "speed": DEFAULT_PRECISION,
            "rate": DEFAULT_PRECISION,
            "default": DEFAULT_PRECISION
            }
        self.time_format = "%Y-%m-%dT%H:%M:%SZ"

        self.gpx: Gpx = Gpx()

        if self.file_path != "":
            self.parse()

    def check_schema(self):
        pass

    def find_precision(self, number: str) -> int:
        """
        Find decimal precision of a given number.

        Args:
            number (str): Number.

        Returns:
            int: Decimal precision.
        """
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
        """
        Find decimal precision of any type of value in a GPX file (latitude, elevation...).
        """
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

    def find_time_element(self) -> Union[str, None]:
        """
        Find a time element in GPX file.

        Returns:
            Union[str, None]: Time element.
        """
        # Use time from metadata
        metadata = self.gpx_root.find("topo:metadat", self.name_space)
        time = self.find_text(metadata, "topo:time")
        if time is not None:
            return time

        # Use time from track point
        track = self.gpx_root.findall("topo:trk", self.name_space)[0]
        segment = track.findall("topo:trkseg", self.name_space)[0]
        point = segment.findall("topo:trkpt", self.name_space)[0]
        time = self.find_text(point, "topo:time")
        if time is not None:
            return time
        
        # No time element at all...
        return None

    def find_time_format(self):
        """
        Find the time format used in GPX file. 
        """
        time = self.find_time_element()
        if time is None:
            logging.warning("No time element in GPX file")
            return

        try:
            d = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
            self.time_format = "%Y-%m-%dT%H:%M:%SZ"
        except:
            self.time_format = "%Y-%m-%dT%H:%M:%S.%fZ"

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
            logging.debug(f"{element} has no attribute {sub_element}")
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
            logging.debug(f"{element} has no attribute {sub_element}")
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
            logging.debug(f"{element} has no attribute {sub_element}")
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
            logging.debug(f"{element} has no attribute {sub_element}")
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
            logging.debug(f"{element} has no attribute {sub_element}")
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
            logging.debug(f"{element} has no attribute {sub_element}")
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
            time_ = datetime.strptime(self.find_text(element, sub_element), self.time_format)
        except:
            time_ = None
            logging.debug(f"{element} has no attribute {sub_element}")
        return time_
    
    def parse_properties(self):
        """
        Parse XML properties of GPX file.
        """
        self.gpx.creator = self.gpx_root.attrib["creator"]
        self.gpx.version = self.gpx_root.attrib["version"]
        self.gpx.xmlns = self.gpx_root.tag[1:-4]
        name_spaces = self.gpx_root.get("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation").split(" ")
        self.gpx.xsi_schema_location = [x for x in name_spaces if x != ""]

    def parse_bounds(self, bounds) -> Bounds:
        """
        Parse bounds typed element from GPX file.

        Args:
            bounds (xml.etree.ElementTree.Element): Parsed bounds element.

        Returns:
            Bounds: Bounds instance.
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
        Parse copyright typed element from GPX file.

        Args:
            copyright (xml.etree.ElementTree.Element): Parsed copyright element.

        Returns:
            Copyright: Copyright instance.
        """
        if copyright is None:
            return None
        
        author = self.get_text(copyright, "author")
        year = self.find_text(copyright, "topo:year")
        licence = self.find_text(copyright, "topo:licence")
        return Copyright(author, year, licence)
    
    def parse_email(self, email) -> Email:
        """
        Parse email typed element from GPX file.

        Args:
            email (xml.etree.ElementTree.Element): Parsed email element.

        Returns:
            Email: Email instance.
        """
        if email is None:
            return None
        
        id = self.get_text(email, "id")
        domain = self.get_text(email, "domain")
        return Email(id, domain)
    
    def parse_extensions(self, extensions) -> Extensions:
        """
        Parse extensions typed element from GPX file.

        Args:
            extensions (xml.etree.ElementTree.Element): Parsed extensions element.

        Returns:
            Extensions: Extensions instance.
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
        Parse link typed element from GPX file.

        Args:
            link (xml.etree.ElementTree.Element): Parsed link element.

        Returns:
            Link: Link instance.
        """
        if link is None:
            return None
        
        href = self.get_text(link, "href")
        text = self.find_text(link, "topo:text")
        type = self.find_text(link, "topo:type")
        return Link(href, text, type)
    
    def parse_person(self, person) -> Person:
        """
        Parse person typed element from GPX file.

        Args:
            person (xml.etree.ElementTree.Element): Parsed person element.

        Returns:
            Person: Person instance.
        """
        if person is None:
            return None
        
        name = self.find_text(person, "topo:name")
        email = self.parse_email(person.find("topo:email", self.name_space))
        link = self.parse_link(person.find("topo:link", self.name_space))
        return Person(name, email, link)
    
    def parse_metadata(self):
        """
        Parse metadata typed element from GPX file.
        """
        metadata = self.gpx_root.find("topo:metadata", self.name_space)

        name = self.find_text(metadata, "topo:name")
        desc = self.find_text(metadata, "topo:desc")
        author = self.parse_person(metadata.find("topo:author", self.name_space))
        copyright = self.parse_copyright(metadata.find("topo:copyright", self.name_space))
        link = self.parse_link(metadata.find("topo:link", self.name_space))
        time = datetime.strptime(metadata.find("topo:time", self.name_space).text, self.time_format)
        keywords = self.find_text(metadata, "topo:keywords")
        bounds = self.parse_bounds(metadata.find("topo:bounds", self.name_space))
        extensions = self.parse_extensions(metadata.find("topo:extensions", self.name_space))

        self.gpx.metadata = Metadata(name, desc, author, copyright, link, time, keywords, bounds, extensions)

    def parse_way_point(self, way_point) -> WayPoint:
        """
        Parse wpt typed element from GPX file.

        Args:
            way_point (xml.etree.ElementTree.Element): Parsed wpt element.

        Returns:
            WayPoint: WayPoint instance.
        """
        lat = self.get_float(way_point, "lat")
        lon = self.get_float(way_point, "lon")
        ele = self.find_float(way_point, "topo:ele")
        time = self.find_time(way_point, "topo:time")
        mag_var = self.find_float(way_point, "topo:magvar")
        geo_id_height = self.find_float(way_point, "topo:geoidheight")
        geo_id_height = self.find_float(way_point, "topo:geoidheight")
        name = self.find_text(way_point, "topo:name")
        cmt = self.find_text(way_point, "topo:cmt")
        desc = self.find_text(way_point, "topo:desc")
        src = self.find_text(way_point, "topo:src")
        link = self.parse_link(way_point.find("topo:link", self.name_space))
        sym = self.find_text(way_point, "topo:sym")
        type = self.find_text(way_point, "topo:type")
        fix = self.find_text(way_point, "topo:fix")
        sat = self.find_int(way_point, "topo:sat")
        hdop = self.find_float(way_point, "topo:hdop")
        vdop = self.find_float(way_point, "topo:vdop")
        pdop = self.find_float(way_point, "topo:pdop")
        age_of_gps_data = self.find_float(way_point, "topo:ageofgpsdata")
        dgpsid = self.find_float(way_point, "topo:dgpsid")
        extensions = self.parse_extensions(way_point.find("topo:extensions", self.name_space))

        return WayPoint(lat, lon, ele, time, mag_var, geo_id_height, name, cmt, desc, src, link, sym, type, fix, sat, hdop, vdop, pdop, age_of_gps_data, dgpsid, extensions)

    def parse_way_points(self):
        """
        Parse wpt typed elements from GPX file.
        """
        way_points = self.gpx_root.findall("topo:wpt", self.name_space)
        for way_point in way_points:
            self.gpx.wpt.append(self.parse_way_point(way_point))

    def parse_route(self, route) -> Route:
        """
        Parse rte typed element from GPX file.

        Args:
            route (xml.etree.ElementTree.Element): Parsed rte element.

        Returns:
            Route: Route instance.
        """
        name = self.find_text(route, "topo:name")
        cmt = self.find_text(route, "topo:cmt")
        desc = self.find_text(route, "topo:desc")
        src = self.find_text(route, "topo:src")
        link = self.parse_link(route.find("topo:link", self.name_space))
        number = self.find_int(route, "topo:number")
        type = self.find_text(route, "topo:type")
        extensions = self.parse_extensions(route.find("topo:extensions", self.name_space))

        rtept = []
        way_points = route.findall("topo:rtept", self.name_space)
        for way_point in way_points:
            rtept.append(self.parse_way_point(way_point))

        return Route(name, cmt, desc, src, link, number, type, extensions, rtept)

    def parse_routes(self):
        """
        Parse rte typed elements from GPX file
        """
        routes = self.gpx_root.findall("topo:rte", self.name_space)
        for route in routes:
            self.gpx.rte.append(self.parse_route(route))  

    def parse_point(self, point) -> TrackPoint:
        """
        Parse trkpt typed element from GPX file.

        Args:
            point (xml.etree.ElementTree.Element): Parsed trkpt element.

        Returns:
            TrackPoint: TrackPoint instance.
        """
        lat = self.get_float(point, "lat")
        lon = self.get_float(point, "lon")
        ele = self.find_float(point, "topo:ele")
        time = self.find_time(point, "topo:time")

        return TrackPoint(lat, lon, ele, time)

    def parse_segment(self, segment) -> TrackSegment:
        """
        Parse trkseg typed element from GPX file.

        Args:
            segment (xml.etree.ElementTree.Element): Parsed trkseg element.

        Returns:
            TrackSegment: TrackSegment instance.
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
        Parse trk typed element from GPX file.

        Args:
            track (xml.etree.ElementTree.Element): Parsed trk element.

        Returns:
            Track: Track instance.
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
        Parse trk typed elements from GPX file.
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
            Gpx: Gpx instance., self.name_space).text
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

        # Find precisions
        self.find_precisions()

        # Find time format
        self.find_time_format()
        
        # Parse metadata
        try:
            self.parse_metadata()
        except:
            logging.exception("Unable to parse metadata in GPX file")
            raise

        # Parse way points
        try:
            self.parse_way_points()
        except:
            logging.exception("Unable to parse way_points in GPX file")
            raise

        # Parse routes
        try:
            self.parse_routes()
        except:
            logging.exception("Unable to parse routes in GPX file")
            raise

        # Parse tracks
        try:
            self.parse_tracks()
        except:
            logging.exception("Unable to parse tracks in GPX file")
            raise

        # Parse extensions
        try:
            extensions = self.gpx_root.find("topo:extensions", self.name_space)
            self.gpx.extensions = self.parse_extensions(extensions)
        except:
            logging.exception("Unable to parse extensions in GPX file")
            raise

        logging.debug("Parsing complete")
        return self.gpx