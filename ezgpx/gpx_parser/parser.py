from typing import Optional, Union
import logging
from datetime import datetime
import xml.etree.ElementTree as ET

from ..gpx_elements import Bounds, Copyright, Email, Extensions, Gpx, Link, Metadata, Person, Point, PointSegment, Route, TrackSegment, Track, WayPoint

DEFAULT_PRECISION = 2
DEFAULT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

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
        self.time_format = DEFAULT_TIME_FORMAT

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
        except OSError as err:
            logging.exception(f"OS error: {err}")
        except ValueError:
            logging.exception("Could not convert data ({number}) to a floating point value.")
        except Exception as err:
            logging.exception(f"Unexpected {err=}, {type(err)=}.\nUnable to find precision of number: {number}")
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
            logging.warning("No time element in GPX file.")
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

    def parse_bounds(self, bounds, tag: str ="bounds") -> Union[Bounds, None]:
        """
        Parse boundsType element from GPX file.

        Args:
            bounds (xml.etree.ElementTree.Element): Parsed bounds element.
            tag (str, Optional): XML tag. Defaults to "bounds".

        Returns:
            Bounds: Bounds instance.
        """
        if bounds is None:
            return None

        minlat = self.get_text(bounds, "minlat")
        minlon = self.get_text(bounds, "minlon")
        maxlat = self.get_text(bounds, "maxlat")
        maxlon = self.get_text(bounds, "maxlon")

        return Bounds(tag, minlat, minlon, maxlat, maxlon)
    
    def parse_copyright(self, copyright, tag: str ="copyright") -> Union[Copyright, None]:
        """
        Parse copyrightType element from GPX file.

        Args:
            copyright (xml.etree.ElementTree.Element): Parsed copyright element.
            tag (str, Optional): XML tag. Defaults to "copyright".

        Returns:
            Copyright: Copyright instance.
        """
        if copyright is None:
            return None
        
        author = self.get_text(copyright, "author")
        year = self.find_text(copyright, "topo:year")
        licence = self.find_text(copyright, "topo:licence")

        return Copyright(tag, author, year, licence)
    
    def parse_email(self, email, tag: str ="email") -> Union[Email, None]:
        """
        Parse emailType element from GPX file.

        Args:
            email (xml.etree.ElementTree.Element): Parsed email element.
            tag (str, Optional): XML tag. Defaults to "email".

        Returns:
            Email: Email instance.
        """
        if email is None:
            return None
        
        id = self.get_text(email, "id")
        domain = self.get_text(email, "domain")

        return Email(tag, id, domain)
    
    def parse_extensions(self, extensions, tag: str ="extensions") -> Union[Extensions, None]:
        """
        Parse extensionsType element from GPX file.

        Args:
            extensions (xml.etree.ElementTree.Element): Parsed extensions element.
            tag (str, Optional): XML tag. Defaults to "extensions".

        Returns:
            Extensions: Extensions instance.
        """
        if extensions is None:
            return None
        
        # display_color = self.find_text(extensions, "topo:DisplayColor")
        # distance = self.find_text(extensions, "topo:Distance")
        # total_elapsed_time = self.find_text(extensions, "topo:TotalElapsedTime")
        # moving_time = self.find_text(extensions, "topo:MovingTime")
        # stopped_time = self.find_text(extensions, "topo:StoppedTime")
        # moving_speed = self.find_text(extensions, "topo:MovingSpeed")
        # max_speed = self.find_text(extensions, "topo:MaxSpeed")
        # max_elevation = self.find_text(extensions, "topo:MaxElevation")
        # min_elevation = self.find_text(extensions, "topo:MinElevation")
        # ascent = self.find_text(extensions, "topo:Ascent")
        # descent = self.find_text(extensions, "topo:Descent")
        # avg_ascent_rate = self.find_text(extensions, "topo:AvgAscentRate")
        # max_ascent_rate = self.find_text(extensions, "topo:MaxAscentRate")
        # avg_descent_rate = self.find_text(extensions, "topo:AvgDescentRate")
        # max_descent_rate = self.find_text(extensions, "topo:MaxDescentRate")

        # return Extensions(tag, display_color, distance, total_elapsed_time, moving_time, stopped_time, moving_speed, max_speed, max_elevation, min_elevation, ascent, descent, avg_ascent_rate, max_ascent_rate, avg_descent_rate, max_descent_rate)
        return None
    
    def parse_link(self, link, tag: str ="link") -> Union[Link, None]:
        """
        Parse linkType element from GPX file.

        Args:
            link (xml.etree.ElementTree.Element): Parsed link element.
            tag (str, Optional): XML tag. Defaults to "link".

        Returns:
            Link: Link instance.
        """
        if link is None:
            return None
        
        href = self.get_text(link, "href")
        text = self.find_text(link, "topo:text")
        type = self.find_text(link, "topo:type")

        return Link(tag, href, text, type)
    
    def parse_metadata(self, metadata, tag: str = "metadata") -> Union[Metadata, None]:
        """
        Parse metadataType element from GPX file.

        Args:
            metadata (xml.etree.ElementTree.Element): Parsed metadata element.
            tag (str, Optional): XML tag. Defaults to "metadata".

        Returns:
            Metadata: Metadata instance.
        """
        if metadata is None:
            return None

        name = self.find_text(metadata, "topo:name")
        desc = self.find_text(metadata, "topo:desc")
        author = self.parse_person(metadata.find("topo:author", self.name_space))
        copyright = self.parse_copyright(metadata.find("topo:copyright", self.name_space))
        link = self.parse_link(metadata.find("topo:link", self.name_space))
        time = self.find_time(metadata, "topo:time")
        keywords = self.find_text(metadata, "topo:keywords")
        bounds = self.parse_bounds(metadata.find("topo:bounds", self.name_space))
        extensions = self.parse_extensions(metadata.find("topo:extensions", self.name_space))

        return Metadata(tag, name, desc, author, copyright, link, time, keywords, bounds, extensions)

    def parse_person(self, person, tag: str ="person") -> Union[Person, None]:
        """
        Parse personType element from GPX file.

        Args:
            person (xml.etree.ElementTree.Element): Parsed person element.
            tag (str, Optional): XML tag. Defaults to "person".

        Returns:
            Person: Person instance.
        """
        if person is None:
            return None
        
        name = self.find_text(person, "topo:name")
        email = self.parse_email(person.find("topo:email", self.name_space))
        link = self.parse_link(person.find("topo:link", self.name_space))

        return Person(tag, name, email, link)
    
    def parse_point_segment(self, point_segment, tag: str = "ptseg") -> PointSegment:
        pass

    def parse_point(self, point, tag: str = "pt") -> Union[Point, None]:
        """
        Parse ptType element from GPX file.

        Args:
            point (xml.etree.ElementTree.Element): Parsed pt element.
            tag (str, Optional): XML tag. Defaults to "pt".

        Returns:
            Point: Point instance.
        """
        if point is None:
            return None
        
        lat = self.get_float(point, "lat")
        lon = self.get_float(point, "lon")
        ele = self.find_float(point, "topo:ele")
        time = self.find_time(point, "topo:time")

        return Point(tag, lat, lon, ele, time)
    
    def parse_route(self, route, tag: str = "rte") -> Union[Route, None]:
        """
        Parse rteType element from GPX file.

        Args:
            route (xml.etree.ElementTree.Element): Parsed rte element.
            tag (str, Optional): XML tag. Defaults to "rte".

        Returns:
            Route: Route instance.
        """
        if route is None:
            return None
        
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

        return Route(tag, name, cmt, desc, src, link, number, type, extensions, rtept)

    def parse_track_segment(self, track_segment, tag: str = "trkseg") -> Union[TrackSegment, None]:
        """
        Parse trksegType element from GPX file.

        Args:
            track_segment (xml.etree.ElementTree.Element): Parsed trkseg element.
            tag (str, Optional): XML tag. Defaults to "trkseg".

        Returns:
            TrackSegment: TrackSegment instance.
        """
        if track_segment is None:
            return None
        
        # Points
        trkpt = []
        track_points = track_segment.findall("topo:trkpt", self.name_space)
        for track_point in track_points:
            trkpt.append(self.parse_way_point(track_point, "trkpt"))

        # Extensions
        extensions = self.parse_extensions(track_segment.find("topo:extensions", self.name_space))

        return TrackSegment(tag, trkpt, extensions)

    def parse_track(self, track, tag: str = "trk") -> Union[Track, None]:
        """
        Parse trkType element from GPX file.

        Args:
            track (xml.etree.ElementTree.Element): Parsed trk element.
            tag (str, Optional): XML tag. Defaults to "trk".

        Returns:
            Track: Track instance.
        """
        if track is None:
            return None
        
        name = self.find_text(track, "topo:name")
        cmt = self.find_text(track, "topo:cmt")
        desc = self.find_text(track, "topo:desc")
        src = self.find_text(track, "topo:src")
        link = self.parse_link(track.find("topo:link", self.name_space))
        number = self.find_int(track, "topo:number")
        type = self.find_text(track, "topo:type")
        extensions = self.parse_extensions(track.find("topo:extensions", self.name_space))

        trkseg = []
        segments = track.findall("topo:trkseg", self.name_space)
        for segment in segments:
            trkseg.append(self.parse_track_segment(segment))

        return Track(tag, name, cmt, desc, src, link, number, type, extensions, trkseg)
    
    def parse_way_point(self, way_point, tag: str = "wpt") -> Union[WayPoint, None]:
        """
        Parse wptType element from GPX file.

        Args:
            way_point (xml.etree.ElementTree.Element): Parsed wpt element.
            tag (str, Optional): XML tag. Defaults to "person".

        Returns:
            WayPoint: WayPoint instance.
        """
        if way_point is None:
            return None
        
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

        return WayPoint(tag, lat, lon, ele, time, mag_var, geo_id_height, name, cmt, desc, src, link, sym, type, fix, sat, hdop, vdop, pdop, age_of_gps_data, dgpsid, extensions)

    def find_xmlns_xsi(self) -> Union[str, None]:
        schema_location = None
        for elmt in list(self.gpx_root.attrib.keys()):
            if elmt.endswith("schemaLocation"):
                schema_location = elmt[1:-15]
        return schema_location

    def parse_root_properties(self):
        """
        Parse XML properties from GPX file.
        """
        self.gpx.creator = self.gpx_root.attrib["creator"]
        self.gpx.version = self.gpx_root.attrib["version"]
        self.gpx.xmlns = self.gpx_root.tag[1:-4]
        self.gpx.xmlns_xsi = self.find_xmlns_xsi()
        self.name_space["topo"] = self.gpx.xmlns
        name_spaces = self.gpx_root.get("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation").split(" ")
        self.gpx.xsi_schema_location = [x for x in name_spaces if x != ""]

    def parse_root_metadata(self):
        """
        Parse metadataType elements from GPX file.
        """
        self.gpx.metadata = self.parse_metadata(self.gpx_root.find("topo:metadata", self.name_space))

    def parse_root_way_points(self):
        """
        Parse wptType elements from GPX file.
        """
        way_points = self.gpx_root.findall("topo:wpt", self.name_space)
        for way_point in way_points:
            self.gpx.wpt.append(self.parse_way_point(way_point))

    def parse_root_routes(self):
        """
        Parse rteType elements from GPX file
        """
        routes = self.gpx_root.findall("topo:rte", self.name_space)
        for route in routes:
            self.gpx.rte.append(self.parse_route(route))  

    def parse_root_tracks(self):
        """
        Parse trkType elements from GPX file.
        """
        tracks = self.gpx_root.findall("topo:trk", self.name_space)
        for track in tracks:
            self.gpx.tracks.append(self.parse_track(track))

    def parse_root_extensions(self):
        """
        Parse extensionsType elements from GPX file.
        """
        extensions = self.gpx_root.find("topo:extensions", self.name_space)
        self.gpx.extensions = self.parse_extensions(extensions)

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
            logging.error("No GPX file to parse.")
            return

        # Parse GPX file
        try:
            self.gpx_tree = ET.parse(self.file_path)
            self.gpx_root = self.gpx_tree.getroot()
        except Exception as err:
            logging.exception(f"Unexpected {err}, {type(err)}.\nUnable to parse GPX file.")
            raise

        # Parse properties
        try:
            self.parse_root_properties()
        except:
            logging.error("Unable to parse properties in GPX file.")
            raise

        # Find precisions
        self.find_precisions()

        # Find time format
        self.find_time_format()
        
        # Parse metadata
        try:
            self.parse_root_metadata()
        except:
            logging.error("Unable to parse metadata in GPX file.")
            raise

        # Parse way points
        try:
            self.parse_root_way_points()
        except:
            logging.error("Unable to parse way_points in GPX file.")
            raise

        # Parse routes
        try:
            self.parse_root_routes()
        except:
            logging.error("Unable to parse routes in GPX file.")
            raise

        # Parse tracks
        try:
            self.parse_root_tracks()
        except:
            logging.error("Unable to parse tracks in GPX file.")
            raise

        # Parse extensions
        try:
            self.parse_root_extensions()
        except:
            logging.error("Unable to parse extensions in GPX file.")
            raise

        logging.debug("Parsing complete!!")
        return self.gpx