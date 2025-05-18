import os
from typing import Optional, Union
import logging
from datetime import datetime
import xml.etree.ElementTree as ET

from .parser import POSSIBLE_TIME_FORMATS
from .xml_parser import XMLParser
from ..gpx_elements import (Bounds, Copyright, Email, Extensions, Gpx, Link,
                            Metadata, Person, Point, PointSegment, Route,
                            TrackSegment, Track, WayPoint)


class GPXParser(XMLParser):
    """
    GPX file parser.
    """

    def __init__(
            self,
            file_path: Optional[str] = None,
            xml_schemas: bool = True,
            xml_extensions_schemas: bool = False) -> None:
        """
        Initialize GPXParser instance.

        Parameters
        ----------
        file_path : Optional[str], optional
            Path to the file to parse, by default None
        xml_schemas : bool, optional
            Toggle schema verification during parsing, by default True
        xml_extensions_schemas : bool, optional
            Toggle extensions schema verificaton durign parsing.
            Requires internet connection and is not guaranted
            to work., by default False
        """
        if not file_path.endswith(".gpx"):
            return

        super().__init__(file_path,
                         xml_schemas,
                         xml_extensions_schemas)

        if self.file_path is not None and os.path.exists(self.file_path):
            self.parse()
        else:
            logging.warning("File path does not exist")

    def _find_precisions(self):
        """
        Find decimal precision of any type of value in a GPX file (latitude, elevation...).
        Also find if the GPX file contains elevation data.
        """
        # Point
        track = self.xml_root.findall("trk", self.name_spaces)[0]
        segment = track.findall("trkseg", self.name_spaces)[0]
        point = segment.findall("trkpt", self.name_spaces)[0]

        ele_text = point.findtext("ele", namespaces=self.name_spaces)
        if ele_text is not None:
            self.ele_data = True
        else:
            self.ele_data = False

        self.precisions["lat_lon"] = self.find_precision(point.get("lat"))
        self.precisions["elevation"] = self.find_precision(ele_text)

    def _find_time_element(self) -> Union[str, None]:
        """
        Find a time element in GPX file.

        Returns:
            Union[str, None]: Time element.
        """
        # Use time from metadata
        metadata = self.xml_root.find("metadata", self.name_spaces)
        if metadata is not None:
            time_str = metadata.findtext("time", namespaces=self.name_spaces)
            if time_str is not None:
                return time_str

        # Use time from track point
        track = self.xml_root.findall("trk", self.name_spaces)[0]  # Optimise, load only once??
        segment = track.findall("trkseg", self.name_spaces)[0]
        point = segment.findall("trkpt", self.name_spaces)[0]
        time_str = point.findtext("time", namespaces=self.name_spaces)
        if time_str is not None:
            return time_str

        # No time element at all...
        return None

    def _find_time_format(self):
        """
        Find the time format used in GPX file.
        Also find if the GPX file contains time data.
        """
        time_str = self._find_time_element()
        if time_str is None:
            self.time_data = False
            logging.warning("No time element in GPX file.")
            return

        self.time_data = True
        for tf in POSSIBLE_TIME_FORMATS:
            try:
                datetime.strptime(time_str, tf)
                self.time_format = tf
                break
            except ValueError:
                pass
        else:
            logging.info("Unknown time format. "
                         "Default time format will be used uppon writting.")

    def _parse_bounds(self, bounds, tag: str = "bounds") -> Union[Bounds, None]:
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

        minlat = bounds.get("minlat")
        minlon = bounds.get("minlon")
        maxlat = bounds.get("maxlat")
        maxlon = bounds.get("maxlon")

        return Bounds(tag, minlat, minlon, maxlat, maxlon)

    def _parse_copyright(self, copyright_, tag: str = "copyright") -> Union[Copyright, None]:
        """
        Parse copyrightType element from GPX file.

        Args:
            copyright (xml.etree.ElementTree.Element): Parsed copyright element.
            tag (str, Optional): XML tag. Defaults to "copyright".

        Returns:
            Copyright: Copyright instance.
        """
        if copyright_ is None:
            return None

        author = copyright_.get("author")
        year = copyright_.findtext("year", namespaces=self.name_spaces)
        licence = copyright_.findtext("licence", namespaces=self.name_spaces)

        return Copyright(tag, author, year, licence)

    def _parse_email(self, email, tag: str = "email") -> Union[Email, None]:
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

        id_ = email.get("id")
        domain = email.get("domain")

        return Email(tag, id_, domain)

    def _parse_extensions(
            self, extensions, element_type: str,
            tag: str = "extensions") -> Union[Extensions, None]:
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

        def construct_dict(e0):
            e1s = [e1 for e1 in e0.iter()][1:]
            if len(e1s) > 0:
                d = {"attrib": dict(e0.items()),
                     "elmts": {}}
                for e1 in e1s:
                    d["elmts"][e1.tag] = construct_dict(e1)
                return d
            else:
                return {"attrib": {},
                        "elmts": e0.text}

        ext = [e for e in extensions.iter()][1]
        values = {ext.tag: {}}
        values[ext.tag] = construct_dict(ext)

        # Etensions fields are based on the first occurance of a type encountered in the file
        if self.extensions_fields.get(element_type) is None:
            self.extensions_fields[element_type] = values

        return Extensions(tag, values)

    def _parse_link(self, link, tag: str = "link") -> Union[Link, None]:
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

        href = link.get("href")
        text = link.findtext("text", namespaces=self.name_spaces)
        type_ = link.findtext("type", namespaces=self.name_spaces)

        return Link(tag, href, text, type_)

    def _parse_metadata(self, metadata, tag: str = "metadata") -> Union[Metadata, None]:
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

        name = metadata.findtext("name", namespaces=self.name_spaces)
        desc = metadata.findtext("desc", namespaces=self.name_spaces)
        author = self._parse_person(metadata.find("author", self.name_spaces))
        copyright_ = self._parse_copyright(
            metadata.find("copyright", self.name_spaces))
        link = self._parse_link(metadata.find("link", self.name_spaces))
        time = self.find_time(metadata, "time")
        keywords = metadata.findtext("keywords", namespaces=self.name_spaces)
        bounds = self._parse_bounds(metadata.find("bounds", self.name_spaces))
        extensions = self._parse_extensions(
            metadata.find("extensions", self.name_spaces), tag)

        return Metadata(tag, name, desc, author, copyright_, link, time,
                        keywords, bounds, extensions)

    def _parse_person(self, person, tag: str = "person") -> Union[Person, None]:
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

        name = person.findtext("name", namespaces=self.name_spaces)
        email = self._parse_email(person.find("email", self.name_spaces))
        link = self._parse_link(person.find("link", self.name_spaces))

        return Person(tag, name, email, link)

    def _parse_point_segment(self, point_segment, tag: str = "ptseg") -> Union[PointSegment, None]:
        """
        Parse ptsegType element from GPX file.

        Parameters
        ----------
        point_segment : xml.etree.ElementTree.Element
            Parsed point segment element
        tag : str, optional
            XML tag, by default "ptseg"

        Returns
        -------
        Union[PointSegment, None]
            PointSegment instance
        """
        if point_segment is None:
            return None

        pt = [self._parse_point(p) for p in point_segment.findall("pt")]

        return PointSegment(tag, pt)

    def _parse_point(self, point, tag: str = "pt") -> Union[Point, None]:
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
        ele = self.find_float(point, "ele")
        time = self.find_time(point, "time")

        return Point(tag, lat, lon, ele, time)

    def _parse_route(self, route, tag: str = "rte") -> Union[Route, None]:
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

        name = route.findtext("name", namespaces=self.name_spaces)
        cmt = route.findtext("cmt", namespaces=self.name_spaces)
        desc = route.findtext("desc", namespaces=self.name_spaces)
        src = route.findtext("src", namespaces=self.name_spaces)
        link = self._parse_link(route.find("link", self.name_spaces))
        number = self.find_int(route, "number")
        type_ = route.findtext("type", namespaces=self.name_spaces)
        extensions = self._parse_extensions(
            route.find("extensions", self.name_spaces), tag)
        rtept = [self._parse_way_point(way_point) for way_point in route.findall(
            "rtept", self.name_spaces)]

        return Route(tag, name, cmt, desc, src, link, number, type_, extensions, rtept)

    def _parse_track_segment(self, track_segment, tag: str = "trkseg") -> Union[TrackSegment, None]:
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

        trkpt = [self._parse_way_point(track_point, "trkpt")
                 for track_point in track_segment.findall("trkpt", self.name_spaces)]
        extensions = self._parse_extensions(
            track_segment.find("extensions", self.name_spaces), tag)

        return TrackSegment(tag, trkpt, extensions)

    def _parse_track(self, track, tag: str = "trk") -> Union[Track, None]:
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

        name = track.findtext("name", namespaces=self.name_spaces)
        cmt = track.findtext("cmt", namespaces=self.name_spaces)
        desc = track.findtext("desc", namespaces=self.name_spaces)
        src = track.findtext("src", namespaces=self.name_spaces)
        link = self._parse_link(track.find("link", self.name_spaces))
        number = self.find_int(track, "number")
        type_ = track.findtext("type", namespaces=self.name_spaces)
        extensions = self._parse_extensions(
            track.find("extensions", self.name_spaces), tag)
        trkseg = [self._parse_track_segment(
            segment) for segment in track.findall("trkseg", self.name_spaces)]

        return Track(tag, name, cmt, desc, src, link, number, type_, extensions, trkseg)

    def _parse_way_point(self, way_point, tag: str = "wpt") -> Union[WayPoint, None]:
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
        ele = self.find_float(way_point, "ele")
        time = self.find_time(way_point, "time")
        mag_var = self.find_float(way_point, "magvar")
        geo_id_height = self.find_float(way_point, "geoidheight")
        geo_id_height = self.find_float(way_point, "geoidheight")
        name = way_point.findtext("name", namespaces=self.name_spaces)
        cmt = way_point.findtext("cmt", namespaces=self.name_spaces)
        desc = way_point.findtext("desc", namespaces=self.name_spaces)
        src = way_point.findtext("src", namespaces=self.name_spaces)
        link = self._parse_link(way_point.find("link", self.name_spaces))
        sym = way_point.findtext("sym", namespaces=self.name_spaces)
        type_ = way_point.findtext("type", namespaces=self.name_spaces)
        fix = way_point.findtext("fix", namespaces=self.name_spaces)
        sat = self.find_int(way_point, "sat")
        hdop = self.find_float(way_point, "hdop")
        vdop = self.find_float(way_point, "vdop")
        pdop = self.find_float(way_point, "pdop")
        age_of_gps_data = self.find_float(way_point, "ageofgpsdata")
        dgpsid = self.find_float(way_point, "dgpsid")
        extensions = self._parse_extensions(
            way_point.find("extensions", self.name_spaces), tag)

        return WayPoint(tag, lat, lon, ele, time, mag_var, geo_id_height, name,
                        cmt, desc, src, link, sym, type_, fix, sat, hdop, vdop,
                        pdop, age_of_gps_data, dgpsid, extensions)

    def _parse_root_properties(self):
        """
        Parse XML properties from GPX file.
        """
        self.gpx.creator = self.xml_root.attrib["creator"]
        self.gpx.version = self.xml_root.attrib["version"]
        schema_location = self.xml_root.get(
            "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation").split(" ")
        self.gpx.xsi_schema_location = [x for x in schema_location if x != ""]

    def _parse_root_metadata(self):
        """
        Parse metadataType elements from GPX file.
        """
        self.gpx.metadata = self._parse_metadata(
            self.xml_root.find("metadata", self.name_spaces))

    def _parse_root_way_points(self):
        """
        Parse wptType elements from GPX file.
        """
        way_points = self.xml_root.findall("wpt", self.name_spaces)
        for way_point in way_points:
            self.gpx.wpt.append(self._parse_way_point(way_point))

    def _parse_root_routes(self):
        """
        Parse rteType elements from GPX file
        """
        routes = self.xml_root.findall("rte", self.name_spaces)
        for route in routes:
            self.gpx.rte.append(self._parse_route(route))

    def _parse_root_tracks(self):
        """
        Parse trkType elements from GPX file.
        """
        tracks = self.xml_root.findall("trk", self.name_spaces)
        for track in tracks:
            self.gpx.trk.append(self._parse_track(track))

    def _parse_root_extensions(self):
        """
        Parse extensionsType elements from GPX file.
        """
        extensions = self.xml_root.find("extensions", self.name_spaces)
        self.gpx.extensions = self._parse_extensions(extensions, "gpx")

    def parse(self) -> Gpx:
        """
        Parse GPX file.

        Returns:
            Gpx: Gpx instance.
        """
        # Parse GPX file
        try:
            self.xml_tree = ET.parse(self.file_path)
            self.xml_root = self.xml_tree.getroot()
        except Exception as err:
            logging.exception("Unexpected %s, %s.\n"
                              "Unable to parse GPX file.", err, type(err))
            raise

        # Parse properties
        try:
            self._parse_root_properties()
        except:
            logging.error("Unable to parse properties in GPX file.")
            raise

        # Check XML schemas
        self.check_xml_schemas()

        # Find precisions
        self._find_precisions()

        # Find time format
        self._find_time_format()

        # Parse metadata
        try:
            self._parse_root_metadata()
        except:
            logging.error("Unable to parse metadata in GPX file.")
            raise

        # Parse way points
        try:
            self._parse_root_way_points()
        except:
            logging.error("Unable to parse way_points in GPX file.")
            raise

        # Parse routes
        try:
            self._parse_root_routes()
        except:
            logging.error("Unable to parse routes in GPX file.")
            raise

        # Parse tracks
        try:
            self._parse_root_tracks()
        except:
            logging.error("Unable to parse tracks in GPX file.")
            raise

        # Parse extensions
        try:
            self._parse_root_extensions()
        except:
            logging.error("Unable to parse extensions in GPX file.")
            raise

        logging.debug("Parsing complete!!")
        return self.gpx
