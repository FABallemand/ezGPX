"""
This module contains the GPXParser class.
"""

import warnings
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import IO

from ..complex_types import (
    Bounds,
    Copyright,
    Email,
    Extensions,
    Gpx,
    Link,
    Metadata,
    Person,
    Pt,
    Ptseg,
    Rte,
    Trk,
    Trkseg,
    Wpt,
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
        # Initialise XMLParser and parse GPX file
        super().__init__(source, xml_schemas, xml_extensions_schemas)
        self.parse()

    def _find_precisions(self):
        """
        Find decimal precision of any type of value in a GPX file (latitude, elevation...).
        Also find if the GPX file contains elevation data.
        """
        # TODO use lat/lon from waypoints, points, track points?
        # TODO store coordinates as string to avoid precision?
        # Point
        tracks = self.xml_root.findall("trk", self.xmlns)
        segments = tracks[0].findall("trkseg", self.xmlns) if tracks else []
        points = segments[0].findall("trkpt", self.xmlns) if segments else []
        if points:
            ele_text = points[0].findtext("ele", namespaces=self.xmlns)
            self.ele_data = ele_text is not None
            self.precisions["lat_lon"] = self._find_precision(points[0].get("lat"))
            self.precisions["elevation"] = self._find_precision(ele_text)

    def _find_time_element(self) -> str | None:
        """
        Find a time element in GPX file.

        Returns:
            str | None: Time element.
        """
        # TODO use time from metadata, waypoints, points, track points, other?
        # TODO store times as string to avoid formar?
        # Use time from metadata
        metadata = self.xml_root.find("metadata", self.xmlns)
        if metadata is not None:
            time_str = metadata.findtext("time", namespaces=self.xmlns)
            if time_str is not None:
                return time_str

        # Use time from track point
        tracks = self.xml_root.findall("trk", self.xmlns)
        segments = tracks[0].findall("trkseg", self.xmlns) if tracks else []
        points = segments[0].findall("trkpt", self.xmlns) if segments else []
        if points:
            time_str = points[0].findtext("time", namespaces=self.xmlns)
            if time_str is not None:
                return time_str

        # No time element at all...
        return None

    def _parse_bounds(self, bounds: ET.Element, tag: str = "bounds") -> Bounds | None:
        """
        Parse boundsType element.

        Args:
            bounds (ET.Element): Parsed bounds element.
            tag (str, Optional): XML tag. Defaults to "bounds".

        Returns:
            Bounds | None: Bounds instance.
        """
        if bounds is None:
            return None
        return Bounds(
            bounds.get("minlat"),
            bounds.get("minlon"),
            bounds.get("maxlat"),
            bounds.get("maxlon"),
            tag,
        )

    def _parse_copyright(
        self,
        copyright: ET.Element,  # pylint: disable=redefined-builtin
        tag: str = "copyright",
    ) -> Copyright | None:
        """
        Parse copyrightType element.

        Args:
            copyright (ET.Element): Parsed copyright element.
            tag (str, Optional): XML tag. Defaults to "copyright".

        Returns:
            Copyright | None: Copyright instance.
        """
        if copyright is None:
            return None
        return Copyright(
            copyright.get("author"),
            copyright.findtext("year", namespaces=self.xmlns),
            copyright.findtext("license", namespaces=self.xmlns),
            tag,
        )

    def _parse_email(self, email: ET.Element, tag: str = "email") -> Email | None:
        """
        Parse emailType element.

        Args:
            email (ET.Element): Parsed email element.
            tag (str, Optional): XML tag. Defaults to "email".

        Returns:
            Email | None: Email instance.
        """
        if email is None:
            return None
        return Email(email.get("id"), email.get("domain"), tag)

    def _parse_extensions(
        self, extensions: ET.Element, element_type: str, tag: str = "extensions"
    ) -> Extensions | None:
        """
        Parse extensionsType element.

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

        return Extensions(values, tag)

    def _parse_link(self, link: ET.Element, tag: str = "link") -> Link | None:
        """
        Parse linkType element.

        Args:
            link (ET.Element): Parsed link element.
            tag (str, Optional): XML tag. Defaults to "link".

        Returns:
            Link | None: Link instance.
        """
        if link is None:
            return None
        return Link(
            link.get("href"),
            link.findtext("text", namespaces=self.xmlns),
            link.findtext("type", namespaces=self.xmlns),
            tag,
        )

    def _parse_metadata(
        self, metadata: ET.Element, tag: str = "metadata"
    ) -> Metadata | None:
        """
        Parse metadataType element.

        Args:
            metadata (ET.Element): Parsed metadata element.
            tag (str, Optional): XML tag. Defaults to "metadata".

        Returns:
            Metadata | None: Metadata instance.
        """
        if metadata is None:
            return None
        return Metadata(
            metadata.findtext("name", namespaces=self.xmlns),
            metadata.findtext("desc", namespaces=self.xmlns),
            self._parse_person(metadata.find("author", self.xmlns)),
            self._parse_copyright(metadata.find("copyright", self.xmlns)),
            [self._parse_link(ll) for ll in metadata.findall("link", self.xmlns)],
            self.find_time(metadata, "time"),
            metadata.findtext("keywords", namespaces=self.xmlns),
            self._parse_bounds(metadata.find("bounds", self.xmlns)),
            self._parse_extensions(metadata.find("extensions", self.xmlns), tag),
            tag,
        )

    def _parse_person(self, person: ET.Element, tag: str = "author") -> Person | None:
        """
        Parse personType element.

        Args:
            person (ET.Element): Parsed person element.
            tag (str, Optional): XML tag. Defaults to "person".

        Returns:
            Person | None: Person instance.
        """
        if person is None:
            return None
        return Person(
            person.findtext("name", namespaces=self.xmlns),
            self._parse_email(person.find("email", self.xmlns)),
            self._parse_link(person.find("link", self.xmlns)),
            tag,
        )

    def _parse_point_segment(
        self, point_segment: ET.Element, tag: str = "ptseg"
    ) -> Ptseg | None:
        """
        Parse ptsegType element.

        Args:
            point_segment (ET.Element): Parsed point segment element.
            tag (str, optional): XML tag. Defaults to "ptseg".

        Returns:
            Ptseg | None: Ptseg instance.
        """
        if point_segment is None:
            return None
        return Ptseg([self._parse_point(p) for p in point_segment.findall("pt")], tag)

    def _parse_point(self, point: ET.Element, tag: str = "pt") -> Pt | None:
        """
        Parse ptType element.

        Args:
            point (ET.Element): Parsed point element.
            tag (str, Optional): XML tag. Defaults to "pt".

        Returns:
            Point | None: Point instance.
        """
        if point is None:
            return None
        return Pt(
            point.get("lat"),
            point.get("lon"),
            self.find_float(point, "ele"),
            self.find_time(point, "time"),
            tag,
        )

    def _parse_route(self, route: ET.Element, tag: str = "rte") -> Rte | None:
        """
        Parse rteType element.

        Args:
            route (ET.Element): Parsed route element.
            tag (str, Optional): XML tag. Defaults to "rte".

        Returns:
            Rte | None: Rte instance.
        """
        if route is None:
            return None
        return Rte(
            route.findtext("name", namespaces=self.xmlns),
            route.findtext("cmt", namespaces=self.xmlns),
            route.findtext("desc", namespaces=self.xmlns),
            route.findtext("src", namespaces=self.xmlns),
            [self._parse_link(ll) for ll in route.findall("link", self.xmlns)],
            self.find_int(route, "number"),
            route.findtext("type", namespaces=self.xmlns),
            self._parse_extensions(route.find("extensions", self.xmlns), tag),
            [
                self._parse_waypoint(w, "rtept")
                for w in route.findall("rtept", self.xmlns)
            ],
            tag,
        )

    def _parse_track_segment(
        self, track_segment: ET.Element, tag: str = "trkseg"
    ) -> Trkseg | None:
        """
        Parse trksegType element.

        Args:
            track_segment (ET.Element): Parsed track
                segment element.
            tag (str, Optional): XML tag. Defaults to "trkseg".

        Returns:
            Trkseg | None: Trkseg instance.
        """
        if track_segment is None:
            return None
        return Trkseg(
            [
                self._parse_waypoint(track_point, "trkpt")
                for track_point in track_segment.findall("trkpt", self.xmlns)
            ],
            self._parse_extensions(track_segment.find("extensions", self.xmlns), tag),
            tag,
        )

    def _parse_track(self, track: ET.Element, tag: str = "trk") -> Trk | None:
        """
        Parse trkType element.

        Args:
            track (ET.Element): Parsed track element.
            tag (str, Optional): XML tag. Defaults to "trk".

        Returns:
            Trk | None: Trk instance.
        """
        if track is None:
            return None
        return Trk(
            track.findtext("name", namespaces=self.xmlns),
            track.findtext("cmt", namespaces=self.xmlns),
            track.findtext("desc", namespaces=self.xmlns),
            track.findtext("src", namespaces=self.xmlns),
            [self._parse_link(ll) for ll in track.findall("link", self.xmlns)],
            self.find_int(track, "number"),
            track.findtext("type", namespaces=self.xmlns),
            self._parse_extensions(track.find("extensions", self.xmlns), tag),
            [self._parse_track_segment(t) for t in track.findall("trkseg", self.xmlns)],
            tag,
        )

    def _parse_waypoint(self, waypoint: ET.Element, tag: str = "wpt") -> Wpt | None:
        """
        Parse wptType element.

        Args:
            waypoint (ET.Element): Parsed waypoint element.
            tag (str, Optional): XML tag. Defaults to "wpt".

        Returns:
            Wpt | None: Wpt instance.
        """
        if waypoint is None:
            return None
        return Wpt(
            waypoint.get("lat"),
            waypoint.get("lon"),
            self.find_float(waypoint, "ele"),
            self.find_time(waypoint, "time"),
            self.find_float(waypoint, "magvar"),
            self.find_float(waypoint, "geoidheight"),
            waypoint.findtext("name", namespaces=self.xmlns),
            waypoint.findtext("cmt", namespaces=self.xmlns),
            waypoint.findtext("desc", namespaces=self.xmlns),
            waypoint.findtext("src", namespaces=self.xmlns),
            [self._parse_link(ll) for ll in waypoint.findall("link", self.xmlns)],
            waypoint.findtext("sym", namespaces=self.xmlns),
            waypoint.findtext("type", namespaces=self.xmlns),
            waypoint.findtext("fix", namespaces=self.xmlns),
            self.find_int(waypoint, "sat"),
            self.find_float(waypoint, "hdop"),
            self.find_float(waypoint, "vdop"),
            self.find_float(waypoint, "pdop"),
            self.find_float(waypoint, "ageofdgpsdata"),
            self.find_float(waypoint, "dgpsid"),
            self._parse_extensions(waypoint.find("extensions", self.xmlns), tag),
            tag,
        )

    def _parse_root_properties(self):
        """
        Parse XML properties.
        """
        self.gpx.creator = self.xml_root.attrib["creator"]
        self.gpx.version = self.xml_root.attrib["version"]
        schema_location = self.xml_root.get(
            "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"
        ).split(" ")
        self.gpx.xsi_schema_location = [x for x in schema_location if x != ""]

    def _parse_root_metadata(self):
        """
        Parse metadataType elements.
        """
        self.gpx.metadata = self._parse_metadata(
            self.xml_root.find("metadata", self.xmlns)
        )

    def _parse_root_waypoints(self):
        """
        Parse wptType elements.
        """
        self.gpx.wpt = [
            self._parse_waypoint(w) for w in self.xml_root.findall("wpt", self.xmlns)
        ]

    def _parse_root_routes(self):
        """
        Parse rteType elements from GPX file
        """
        self.gpx.rte = [
            self._parse_route(r) for r in self.xml_root.findall("rte", self.xmlns)
        ]

    def _parse_root_tracks(self):
        """
        Parse trkType elements.
        """
        self.gpx.trk = [
            self._parse_track(t) for t in self.xml_root.findall("trk", self.xmlns)
        ]

    def _parse_root_extensions(self):
        """
        Parse extensionsType elements.
        """
        extensions = self.xml_root.find("extensions", self.xmlns)
        self.gpx.extensions = self._parse_extensions(extensions, "gpx")

    def parse(self) -> Gpx:
        """
        Parse GPX file.

        Returns:
            dict: Gpx instance, precisions and time format.
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
        self._find_time_format(self._find_time_element())

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

        return {
            "gpx": self.gpx,
            "xmlns": self.xmlns,
            "ele_data": self.ele_data,
            "time_data": self.time_data,
            "precisions": self.precisions,
            "time_format": self.time_format,
            "extensions_fields": self.extensions_fields,
        }
