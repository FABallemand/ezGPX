"""
This module contains the GPXParser class.
"""

import io
import warnings
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import IO

from ..constants.precisions import POSSIBLE_TIME_FORMATS
from ..gpx_elements import (
    Bounds,
    Copyright,
    Email,
    Extensions,
    Gpx,
    Link,
    Metadata,
    Person,
    Point,
    PointSegment,
    Route,
    Track,
    TrackSegment,
    WayPoint,
)
from .xml_parser import XMLParser


class GPXParser(XMLParser):
    """
    GPX file parser.
    """

    def __init__(
        self,
        source: str | Path | IO[str] | IO[bytes] | bytes,
        xml_schemas: bool = True,
        xml_extensions_schemas: bool = False,
    ) -> None:
        """
        Initialise GPXParser instance.

        Args:
            source (str | Path | IO[str] | IO[bytes] | bytes): Path to a
                file or a file-like object to parse.
            xml_schemas (bool, optional): Toggle schema
                verification during parsing. Defaults to True.
            xml_extensions_schemas (bool, optional): Toggle extensions
                schema verificaton durign parsing. Requires internet connection
                connection and is not guaranted to work. Defaults to False.
        """
        # Bytes object
        if isinstance(source, bytes):
            source = io.BytesIO(source)

        # Initialise XMLParser and parse GPX file
        super().__init__(source, xml_schemas, xml_extensions_schemas)
        self.parse()

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

    def _find_time_element(self) -> str | None:
        """
        Find a time element in GPX file.

        Returns:
            str | None: Time element.
        """
        # Use time from metadata
        metadata = self.xml_root.find("metadata", self.name_spaces)
        if metadata is not None:
            time_str = metadata.findtext("time", namespaces=self.name_spaces)
            if time_str is not None:
                return time_str

        # Use time from track point
        track = self.xml_root.findall("trk", self.name_spaces)[
            0
        ]  # Optimise, load only once??
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
            warnings.warn("No time element in GPX file.")
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
            warnings.warn(
                """Unknown time format. Default time format will be used uppon
                writting."""
            )

    def _parse_bounds(self, bounds: ET.Element, tag: str = "bounds") -> Bounds | None:
        """
        Parse boundsType element from GPX file.

        Args:
            bounds (ET.Element): Parsed bounds element.
            tag (str, Optional): XML tag. Defaults to "bounds".

        Returns:
            Bounds | None: Bounds instance.
        """
        if bounds is None:
            return None

        return Bounds(
            tag,
            bounds.get("minlat"),
            bounds.get("minlon"),
            bounds.get("maxlat"),
            bounds.get("maxlon"),
        )

    def _parse_copyright(
        self, copyright_: ET.Element, tag: str = "copyright"
    ) -> Copyright | None:
        """
        Parse copyrightType element from GPX file.

        Args:
            copyright (ET.Element): Parsed copyright element.
            tag (str, Optional): XML tag. Defaults to "copyright".

        Returns:
            Copyright | None: Copyright instance.
        """
        if copyright_ is None:
            return None

        return Copyright(
            tag,
            copyright_.get("author"),
            copyright_.findtext("year", namespaces=self.name_spaces),
            copyright_.findtext("licence", namespaces=self.name_spaces),
        )

    def _parse_email(self, email: ET.Element, tag: str = "email") -> Email | None:
        """
        Parse emailType element from GPX file.

        Args:
            email (ET.Element): Parsed email element.
            tag (str, Optional): XML tag. Defaults to "email".

        Returns:
            Email | None: Email instance.
        """
        if email is None:
            return None

        return Email(tag, email.get("id"), email.get("domain"))

    def _parse_extensions(
        self, extensions: ET.Element, element_type: str, tag: str = "extensions"
    ) -> Extensions | None:
        """
        Parse extensionsType element from GPX file.

        Args:
            extensions (ET.Element): Parsed extensions element.
            tag (str, Optional): XML tag. Defaults to "extensions".

        Returns:
            Extensions | None: Extensions instance.
        """
        if extensions is None:
            return None

        def construct_dict(e0):
            e1s = list(e0.iter())[1:]
            if len(e1s) > 0:
                d = {"attrib": dict(e0.items()), "elmts": {}}
                for e1 in e1s:
                    d["elmts"][e1.tag] = construct_dict(e1)
                return d
            return {"attrib": {}, "elmts": e0.text}

        ext = list(extensions.iter())[1]
        values = {ext.tag: {}}
        values[ext.tag] = construct_dict(ext)

        # Etensions fields are based on the first occurance of a type encountered in the file
        if self.extensions_fields.get(element_type) is None:
            self.extensions_fields[element_type] = values

        return Extensions(tag, values)

    def _parse_link(self, link: ET.Element, tag: str = "link") -> Link | None:
        """
        Parse linkType element from GPX file.

        Args:
            link (ET.Element): Parsed link element.
            tag (str, Optional): XML tag. Defaults to "link".

        Returns:
            Link | None: Link instance.
        """
        if link is None:
            return None

        return Link(
            tag,
            link.get("href"),
            link.findtext("text", namespaces=self.name_spaces),
            link.findtext("type", namespaces=self.name_spaces),
        )

    def _parse_metadata(
        self, metadata: ET.Element, tag: str = "metadata"
    ) -> Metadata | None:
        """
        Parse metadataType element from GPX file.

        Args:
            metadata (ET.Element): Parsed metadata element.
            tag (str, Optional): XML tag. Defaults to "metadata".

        Returns:
            Metadata | None: Metadata instance.
        """
        if metadata is None:
            return None

        return Metadata(
            tag,
            metadata.findtext("name", namespaces=self.name_spaces),
            metadata.findtext("desc", namespaces=self.name_spaces),
            self._parse_person(metadata.find("author", self.name_spaces)),
            self._parse_copyright(metadata.find("copyright", self.name_spaces)),
            self._parse_link(metadata.find("link", self.name_spaces)),
            self.find_time(metadata, "time"),
            metadata.findtext("keywords", namespaces=self.name_spaces),
            self._parse_bounds(metadata.find("bounds", self.name_spaces)),
            self._parse_extensions(metadata.find("extensions", self.name_spaces), tag),
        )

    def _parse_person(self, person: ET.Element, tag: str = "person") -> Person | None:
        """
        Parse personType element from GPX file.

        Args:
            person (ET.Element): Parsed person element.
            tag (str, Optional): XML tag. Defaults to "person".

        Returns:
            Person | None: Person instance.
        """
        if person is None:
            return None

        return Person(
            tag,
            person.findtext("name", namespaces=self.name_spaces),
            self._parse_email(person.find("email", self.name_spaces)),
            self._parse_link(person.find("link", self.name_spaces)),
        )

    def _parse_point_segment(
        self, point_segment: ET.Element, tag: str = "ptseg"
    ) -> PointSegment | None:
        """
        Parse ptsegType element from GPX file.

        Args:
            point_segment (ET.Element): Parsed point segment element.
            tag (str, optional): XML tag. Defaults to "ptseg".

        Returns:
            PointSegment | None: PointSegment instance.
        """
        if point_segment is None:
            return None

        return PointSegment(
            tag, [self._parse_point(p) for p in point_segment.findall("pt")]
        )

    def _parse_point(self, point: ET.Element, tag: str = "pt") -> Point | None:
        """
        Parse ptType element from GPX file.

        Args:
            point (ET.Element): Parsed point element.
            tag (str, Optional): XML tag. Defaults to "pt".

        Returns:
            Point | None: Point instance.
        """
        if point is None:
            return None

        return Point(
            tag,
            self.get_float(point, "lat"),
            self.get_float(point, "lon"),
            self.find_float(point, "ele"),
            self.find_time(point, "time"),
        )

    def _parse_route(self, route: ET.Element, tag: str = "rte") -> Route | None:
        """
        Parse rteType element from GPX file.

        Args:
            route (ET.Element): Parsed route element.
            tag (str, Optional): XML tag. Defaults to "rte".

        Returns:
            Route | None: Route instance.
        """
        if route is None:
            return None

        return Route(
            tag,
            route.findtext("name", namespaces=self.name_spaces),
            route.findtext("cmt", namespaces=self.name_spaces),
            route.findtext("desc", namespaces=self.name_spaces),
            route.findtext("src", namespaces=self.name_spaces),
            self._parse_link(route.find("link", self.name_spaces)),
            self.find_int(route, "number"),
            route.findtext("type", namespaces=self.name_spaces),
            self._parse_extensions(route.find("extensions", self.name_spaces), tag),
            [
                self._parse_waypoint(waypoint)
                for waypoint in route.findall("rtept", self.name_spaces)
            ],
        )

    def _parse_track_segment(
        self, track_segment: ET.Element, tag: str = "trkseg"
    ) -> TrackSegment | None:
        """
        Parse trksegType element from GPX file.

        Args:
            track_segment (ET.Element): Parsed track
                segment element.
            tag (str, Optional): XML tag. Defaults to "trkseg".

        Returns:
            TrackSegment | None: TrackSegment instance.
        """
        if track_segment is None:
            return None

        return TrackSegment(
            tag,
            [
                self._parse_waypoint(track_point, "trkpt")
                for track_point in track_segment.findall("trkpt", self.name_spaces)
            ],
            self._parse_extensions(
                track_segment.find("extensions", self.name_spaces), tag
            ),
        )

    def _parse_track(self, track: ET.Element, tag: str = "trk") -> Track | None:
        """
        Parse trkType element from GPX file.

        Args:
            track (ET.Element): Parsed track element.
            tag (str, Optional): XML tag. Defaults to "trk".

        Returns:
            Track | None: Track instance.
        """
        if track is None:
            return None

        return Track(
            tag,
            track.findtext("name", namespaces=self.name_spaces),
            track.findtext("cmt", namespaces=self.name_spaces),
            track.findtext("desc", namespaces=self.name_spaces),
            track.findtext("src", namespaces=self.name_spaces),
            self._parse_link(track.find("link", self.name_spaces)),
            self.find_int(track, "number"),
            track.findtext("type", namespaces=self.name_spaces),
            self._parse_extensions(track.find("extensions", self.name_spaces), tag),
            [
                self._parse_track_segment(segment)
                for segment in track.findall("trkseg", self.name_spaces)
            ],
        )

    def _parse_waypoint(
        self, waypoint: ET.Element, tag: str = "wpt"
    ) -> WayPoint | None:
        """
        Parse wptType element from GPX file.

        Args:
            waypoint (ET.Element): Parsed waypoint element.
            tag (str, Optional): XML tag. Defaults to "wpt".

        Returns:
            WayPoint | None: WayPoint instance.
        """
        if waypoint is None:
            return None

        return WayPoint(
            tag,
            self.get_float(waypoint, "lat"),
            self.get_float(waypoint, "lon"),
            self.find_float(waypoint, "ele"),
            self.find_time(waypoint, "time"),
            self.find_float(waypoint, "magvar"),
            self.find_float(waypoint, "geoidheight"),
            waypoint.findtext("name", namespaces=self.name_spaces),
            waypoint.findtext("cmt", namespaces=self.name_spaces),
            waypoint.findtext("desc", namespaces=self.name_spaces),
            waypoint.findtext("src", namespaces=self.name_spaces),
            self._parse_link(waypoint.find("link", self.name_spaces)),
            waypoint.findtext("sym", namespaces=self.name_spaces),
            waypoint.findtext("type", namespaces=self.name_spaces),
            waypoint.findtext("fix", namespaces=self.name_spaces),
            self.find_int(waypoint, "sat"),
            self.find_float(waypoint, "hdop"),
            self.find_float(waypoint, "vdop"),
            self.find_float(waypoint, "pdop"),
            self.find_float(waypoint, "ageofgpsdata"),
            self.find_float(waypoint, "dgpsid"),
            self._parse_extensions(waypoint.find("extensions", self.name_spaces), tag),
        )

    def _parse_root_properties(self):
        """
        Parse XML properties from GPX file.
        """
        self.gpx.creator = self.xml_root.attrib["creator"]
        self.gpx.version = self.xml_root.attrib["version"]
        schema_location = self.xml_root.get(
            "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"
        ).split(" ")
        self.gpx.xsi_schema_location = [x for x in schema_location if x != ""]

    def _parse_root_metadata(self):
        """
        Parse metadataType elements from GPX file.
        """
        self.gpx.metadata = self._parse_metadata(
            self.xml_root.find("metadata", self.name_spaces)
        )

    def _parse_root_waypoints(self):
        """
        Parse wptType elements from GPX file.
        """
        waypoints = self.xml_root.findall("wpt", self.name_spaces)
        for waypoint in waypoints:
            self.gpx.wpt.append(self._parse_waypoint(waypoint))

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
            self.xml_tree = ET.parse(self.source)
            self.xml_root = self.xml_tree.getroot()
        except Exception as err:
            warnings.warn(f"Unexpected {err}, {type(err)}.\nUnable to parse GPX file.")
            raise

        # Parse properties
        try:
            self._parse_root_properties()
        except Exception as e:
            raise ValueError("Unable to parse properties in GPX file.") from e

        # Check XML schemas
        self.xml_schemas()

        # Find precisions
        self._find_precisions()

        # Find time format
        self._find_time_format()

        # Parse metadata
        try:
            self._parse_root_metadata()
        except:
            warnings.warn("Unable to parse metadata in GPX file.")
            raise

        # Parse way points
        try:
            self._parse_root_waypoints()
        except:
            warnings.warn("Unable to parse waypoints in GPX file.")
            raise

        # Parse routes
        try:
            self._parse_root_routes()
        except:
            warnings.warn("Unable to parse routes in GPX file.")
            raise

        # Parse tracks
        try:
            self._parse_root_tracks()
        except:
            warnings.warn("Unable to parse tracks in GPX file.")
            raise

        # Parse extensions
        try:
            self._parse_root_extensions()
        except:
            warnings.warn("Unable to parse extensions in GPX file.")
            raise

        return self.gpx
