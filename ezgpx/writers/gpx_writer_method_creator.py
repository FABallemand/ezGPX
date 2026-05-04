# ruff: noqa: F401
# pylint: disable=line-too-long
"""
This module contains the GPXWriterMethodCreator class.
"""

import xml.etree.ElementTree as ET  # pylint: disable=unused-import
from types import FunctionType


class GPXWriterMethodCreator:
    """
    GPXWriter method creator.
    """

    def add_bounds_creator(
        self, fields: list
    ) -> FunctionType:  # TODO only mandatory fields -> overhead?
        """
        Create `add_bounds` method.

        Args:
            fields (list): `Bounds` fields.

        Returns:
            FunctionType: `add_bounds` method.
        """
        code = (
            "def _add_bound(writer, element, bounds):"
            "\n\tif bounds is not None:"
            "\n\t\tbounds_ = ET.SubElement(element, bounds.tag)"
        )
        if "minlat" in fields:
            code += '\n\t\twriter.set_not_none(bounds_, "minlat", f"{bounds.minlat.value:.{writer.precisions["lat_lon"]}f}")'
        if "minlon" in fields:
            code += '\n\t\twriter.set_not_none(bounds_, "minlon", f"{bounds.minlon.value:.{writer.precisions["lat_lon"]}f}")'
        if "maxlat" in fields:
            code += '\n\t\twriter.set_not_none(bounds_, "maxlat", f"{bounds.maxlat.value:.{writer.precisions["lat_lon"]}f}")'
        if "maxlon" in fields:
            code += '\n\t\twriter.set_not_none(bounds_, "maxlon", f"{bounds.maxlon.value:.{writer.precisions["lat_lon"]}f}")'
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_bounds>", "exec").co_consts[0],
            globals(),
            "_add_bounds",
        )

    def add_copyright_creator(self, fields: list) -> FunctionType:
        """
        Create `add_copyright` method.

        Args:
            fields (list): `Copyright` fields.

        Returns:
            FunctionType: `add_copyright` method.
        """
        code = (
            "def _add_copyright(writer, element, copyright):"
            "\n\tif copyright is not None:"
            "\n\t\tcopyright_ = ET.SubElement(element, copyright.tag)"
        )
        if "author" in fields:
            code += '\n\t\twriter.set_not_none(copyright_, "author", copyright.author)'
        if "year" in fields:
            code += '\n\t\tcopyright_, _ = writer.add_subelement(copyright_, "year", str(copyright.year))'
        if "license" in fields:
            code += '\n\t\tcopyright_, _ = writer.add_subelement(copyright_, "license", str(copyright.license))'
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_copyright>", "exec").co_consts[0],
            globals(),
            "_add_copyright",
        )

    def add_email_creator(self, fields: list) -> FunctionType:
        """
        Create `add_email` method.

        Args:
            fields (list): `Email` fields.

        Returns:
            FunctionType: `add_email` method.
        """
        code = (
            "def _add_email(writer, element, email):"
            "\n\tif email is not None:"
            "\n\t\temail_ = ET.SubElement(element, email.tag)"
        )
        if "id" in fields:
            code += '\n\t\twriter.set_not_none(email_, "id", email.id)'
        if "domain" in fields:
            code += '\n\t\twriter.set_not_none(email_, "domain", email.domain)'
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_email>", "exec").co_consts[0], globals(), "_add_email"
        )

    # def add_extensions_creator(self, extensions_fields):
    #     code = ('def _add_extensions(writer, element, extensions):'
    #             '\n\tif extensions is not None:'
    #             '\n\t\textensions_ = ET.SubElement(element, extensions.tag)')
    #     if extensions_fields is not None:
    #         for k, v in extensions_fields:
    #             code += f'\n\t\textensions_, _ = writer.add_extensions_element(extensions_, "{k}", extensions.values["{field}"])'
    #     code += '\n\treturn element'
    #     return FunctionType(compile(code, "<_add_extensions>", "exec").co_consts[0], globals(), "_add_extensions")

    def add_link_creator(self, fields: list) -> FunctionType:
        """
        Create `add_link` method.

        Args:
            fields (list): `Link` fields.

        Returns:
            FunctionType: `add_link` method.
        """
        code = (
            "def _add_link(writer, element, link):"
            "\n\tif link is not None:"
            "\n\t\tlink_ = ET.SubElement(element, link.tag)"
        )
        if "href" in fields:
            code += (
                "\n\t\tif link.href is not None:"
                '\n\t\t\twriter.set_not_none(link_, "href", link.href)'
            )
        if "text" in fields:
            code += '\n\t\tlink_, _ = writer.add_subelement(link_, "text", link.text)'
        if "type" in fields:
            code += '\n\t\tlink_, _ = writer.add_subelement(link_, "type", link.type)'
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_link>", "exec").co_consts[0], globals(), "_add_link"
        )

    def add_metadata_creator(self, fields: list[str]):
        """
        Create `add_metadata` method.

        Args:
            fields (list): `Metadata` fields.

        Returns:
            FunctionType: `add_metadata` method.
        """
        code = (
            "def _add_metadata(writer, element, metadata):"
            "\n\tif metadata is not None:"
            "\n\t\tmetadata_ = ET.SubElement(element, metadata.tag)"
        )
        if "name" in fields:
            code += '\n\t\tmetadata_, _ = writer.add_subelement(metadata_, "name", metadata.name)'
        if "desc" in fields:
            code += '\n\t\tmetadata_, _ = writer.add_subelement(metadata_, "desc", metadata.desc)'
        if "author" in fields:
            code += "\n\t\tmetadata_ = writer.add_person(metadata_, metadata.author)"
        if "copyright" in fields:
            code += (
                "\n\t\tmetadata_ = writer.add_copyright(metadata_, metadata.copyright)"
            )
        if "link" in fields:
            code += "\n\t\tfor l in metadata.link:"
            code += "\n\t\t\tmetadata_ = writer.add_link(metadata_, l)"
        if "time" in fields:
            code += '\n\t\tmetadata_, _ = writer.add_subelement_time(metadata_, "time", metadata.time, writer.time_format)'
        if "keywords" in fields:
            code += '\n\t\tmetadata_, _ = writer.add_subelement(metadata_, "keywords", metadata.keywords)'
        if "bounds" in fields:
            code += "\n\t\tmetadata_ = writer.add_bounds(metadata_, metadata.bounds)"
        if "extensions" in fields:
            # code += '\n\t\tmetadata_ = writer.add_metadata_extensions(metadata_, metadata.extensions)'
            code += '\n\t\tmetadata_ = writer.add_extensions(metadata_, metadata.extensions, writer.extensions_fields.get("metadata"))'
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_metadata>", "exec").co_consts[0],
            globals(),
            "_add_metadata",
        )

    def add_person_creator(self, fields: list) -> FunctionType:
        """
        Create `add_person` method.

        Args:
            fields (list): `Person` fields.

        Returns:
            FunctionType: `add_person` method.
        """
        code = (
            "def _add_person(writer, element, person):"
            "\n\tif person is not None:"
            "\n\t\tperson_ = ET.SubElement(element, person.tag)"
        )
        if "name" in fields:
            code += (
                '\n\t\tperson_, _ = writer.add_subelement(person_, "name", person.name)'
            )
        if "email" in fields:
            code += "\n\t\tperson_ = writer.add_email(person_, person.email)"
        if "link" in fields:
            code += "\n\t\tperson_ = writer.add_link(person_, person.link)"
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_person>", "exec").co_consts[0],
            globals(),
            "_add_person",
        )

    def add_point_segment_creator(self, fields: list) -> FunctionType:
        """
        Create `add_point_segment` method.

        Args:
            fields (list): `Ptseg` fields.

        Returns:
            FunctionType: `add_point_segment` method.
        """
        code = (
            "def _add_point_segment(writer, element, point_segment):"
            "\n\tif point_segment is not None:"
            "\n\t\tpoint_segment_ = ET.SubElement(element, point_segment.tag)"
        )
        if "pt" in fields:
            code += (
                "\n\t\tfor point in point_segment.pt:"
                "\n\t\t\tpoint_segment_ = writer.add_point(point_segment_, point)"
            )
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_point_segment>", "exec").co_consts[0],
            globals(),
            "_add_point_segment",
        )

    def add_point_creator(self, fields: list) -> FunctionType:
        """
        Create `add_point` method.

        Args:
            fields (list): `Pt` fields.

        Returns:
            FunctionType: `add_point` method.
        """
        code = (
            "def _add_point(writer, element, point):"
            "\n\tif point is not None:"
            "\n\t\tpoint_ = ET.SubElement(element, point.tag)"
        )
        if "lat" in fields:
            code += '\n\t\twriter.set_not_none(point_, "lat", "{:.{}f}".format(point.lat.value, writer.precisions["lat_lon"]))'
        if "lon" in fields:
            code += '\n\t\twriter.set_not_none(point_, "lon", "{:.{}f}".format(point.lon.value, writer.precisions["lat_lon"]))'
        if "ele" in fields:
            code += '\n\t\tpoint_ = writer.add_subelement_number(point_, "ele", point.ele, writer.precisions["elevation"])'
        if "time" in fields:
            code += '\n\t\tpoint_, _ = writer.add_subelement_time(point_, "time", point.time, writer.time_format)'
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_point>", "exec").co_consts[0], globals(), "_add_point"
        )

    def add_route_creator(self, fields: list) -> FunctionType:
        """
        Create `add_route` method.

        Args:
            fields (list): `Rte` fields.

        Returns:
            FunctionType: `add_route` method.
        """
        code = (
            "def _add_route(writer, element, route):"
            "\n\tif route is not None:"
            "\n\t\troute_ = ET.SubElement(element, route.tag)"
        )
        if "name" in fields:
            code += (
                '\n\t\troute_, _ = writer.add_subelement(route_, "name", route.name)'
            )
        if "cmt" in fields:
            code += '\n\t\troute_, _ = writer.add_subelement(route_, "cmt", route.cmt)'
        if "desc" in fields:
            code += (
                '\n\t\troute_, _ = writer.add_subelement(route_, "desc", route.desc)'
            )
        if "src" in fields:
            code += '\n\t\troute_, _ = writer.add_subelement(route_, "src", route.src)'
        if "link" in fields:
            code += "\n\t\tfor l in route.link:"
            code += "\n\t\t\troute_ = writer.add_link(route_, l)"
        if "number" in fields:
            code += '\n\t\troute_, _ = writer.add_subelement_number(route_, "number", route.number)'
        if "type" in fields:
            code += (
                '\n\t\troute_, _ = writer.add_subelement(route_, "type", route.type)'
            )
        if "extensions" in fields:
            # code += '\n\t\troute_ = writer.add_rte_extensions(route_, route.extensions)'
            code += '\n\t\troute_ = writer.add_extensions(route_, route.extensions, writer.extensions_fields.get("rte"))'
        if "rtept" in fields:
            code += (
                "\n\t\tfor waypoint in route.rtept:"
                "\n\t\t\troute_ = writer.add_waypoint(route_, waypoint)"
            )
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_route>", "exec").co_consts[0], globals(), "_add_route"
        )

    def add_track_segment_creator(self, fields: list) -> FunctionType:
        """
        Create `add_track_segment` method.

        Args:
            fields (list): `Trkseg` fields.

        Returns:
            FunctionType: `add_track_segment` method.
        """
        code = (
            "def _add_track_segment(writer, element, track_segment):"
            "\n\tif track_segment is not None:"
            "\n\t\ttrack_segment_ = ET.SubElement(element, track_segment.tag)"
        )
        if "extensions" in fields:
            # code += '\n\t\ttrack_segment_ = writer.add_trkseg_extensions(track_segment_, track_segment.extensions)'
            code += '\n\t\ttrack_segment_ = writer.add_extensions(track_segment_, track_segment.extensions, writer.extensions_fields.get("trkseg"))'
        if "trkpt" in fields:
            code += (
                "\n\t\tfor track_point in track_segment.trkpt:"
                "\n\t\t\ttrack_segment_ = writer.add_track_point(track_segment_, track_point)"
            )
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_track_segment>", "exec").co_consts[0],
            globals(),
            "_add_track_segment",
        )

    def add_track_creator(self, fields: list) -> FunctionType:
        """
        Create `add_track` method.

        Args:
            fields (list): `Trk` fields.

        Returns:
            FunctionType: `add_track` method.
        """
        code = (
            "def _add_track(writer, element, track):"
            "\n\tif track is not None:"
            "\n\t\ttrack_ = ET.SubElement(element, track.tag)"
        )
        if "name" in fields:
            code += (
                '\n\t\ttrack_, _ = writer.add_subelement(track_, "name", track.name)'
            )
        if "cmt" in fields:
            code += '\n\t\ttrack_, _ = writer.add_subelement(track_, "cmt", track.cmt)'
        if "desc" in fields:
            code += (
                '\n\t\ttrack_, _ = writer.add_subelement(track_, "desc", track.desc)'
            )
        if "src" in fields:
            code += '\n\t\ttrack_, _ = writer.add_subelement(track_, "src", track.src)'
        if "link" in fields:
            code += "\n\t\tfor l in track.link:"
            code += "\n\t\t\ttrack_ = writer.add_link(track_, l)"
        if "number" in fields:
            code += '\n\t\ttrack_, _ = writer.add_subelement_number(track_, "number", track.number)'
        if "type" in fields:
            code += (
                '\n\t\ttrack_, _ = writer.add_subelement(track_, "type", track.type)'
            )
        if "extensions" in fields:
            # code += '\n\t\ttrack_ = writer.add_trk_extensions(track_, track.extensions)'
            code += '\n\t\ttrack_ = writer.add_extensions(track_, track.extensions, writer.extensions_fields.get("trk"))'
        if "trkseg" in fields:
            code += (
                "\n\t\tfor track_seg in track.trkseg:"
                "\n\t\t\ttrack_ = writer.add_track_segment(track_, track_seg)"
            )
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_track>", "exec").co_consts[0], globals(), "_add_track"
        )

    def add_waypoint_creator(self, fields: list) -> FunctionType:
        """
        Create `add_waypoint` method.

        Args:
            fields (list): `Wpt` fields.

        Returns:
            FunctionType: `add_waypoint` method.
        """
        code = (
            "def _add_waypoint(writer, element, waypoint):"
            "\n\tif waypoint is not None:"
            "\n\t\twaypoint_ = ET.SubElement(element, waypoint.tag)"
        )
        if "lat" in fields:
            code += '\n\t\twriter.set_not_none(waypoint_, "lat", "{:.{}f}".format(waypoint.lat.value, writer.precisions["lat_lon"]))'
        if "lon" in fields:
            code += '\n\t\twriter.set_not_none(waypoint_, "lon", "{:.{}f}".format(waypoint.lon.value, writer.precisions["lat_lon"]))'
        if "ele" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "ele", waypoint.ele, writer.precisions["elevation"])'
        if "time" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_time(waypoint_, "time", waypoint.time, writer.time_format)'
        if "magvar" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "magvar", waypoint.magvar.value, writer.precisions["default"])'
        if "geoidheight" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "geoidheight", waypoint.geoidheight, writer.precisions["default"])'
        if "name" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "name", waypoint.name)'
        if "cmt" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "cmt", waypoint.cmt)'
        if "desc" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "desc", waypoint.desc)'
        if "src" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "src", waypoint.src)'
        if "link" in fields:
            code += "\n\t\tfor l in waypoint.link:"
            code += "\n\t\t\twaypoint_ = writer.add_link(waypoint_, l)"
        if "sym" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "sym", waypoint.sym)'
        if "type" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "type", waypoint.type)'
        if "fix" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "fix", waypoint.fix.value)'
        if "sat" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "sat", waypoint.sat, 0)'
        if "hdop" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "hdop", waypoint.hdop, writer.precisions["default"])'
        if "vdop" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "vdop", waypoint.vdop, writer.precisions["default"])'
        if "pdop" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "pdop", waypoint.pdop, writer.precisions["default"])'
        if "ageofdgpsdata" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "ageofdgpsdata", waypoint.ageofdgpsdata, writer.precisions["default"])'
        if "dgpsid" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "dgpsid", waypoint.dgpsid.value, 0)'
        if "extensions" in fields:
            # code += '\n\t\twaypoint_ = writer.add_wpt_extensions(waypoint_, waypoint.extensions)'
            code += '\n\t\twaypoint_ = writer.add_extensions(waypoint_, waypoint.extensions, writer.extensions_fields.get("wpt"))'
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_waypoint>", "exec").co_consts[0],
            globals(),
            "_add_waypoint",
        )

    def add_track_point_creator(self, fields: list) -> FunctionType:
        """
        Create `add_waypoint` method.

        Args:
            fields (list): `Wpt` fields.

        Returns:
            FunctionType: `add_waypoint` method.
        """
        code = (
            "def _add_track_point(writer, element, waypoint):"
            "\n\tif waypoint is not None:"
            "\n\t\twaypoint_ = ET.SubElement(element, waypoint.tag)"
        )
        if "lat" in fields:
            code += '\n\t\twriter.set_not_none(waypoint_, "lat", "{:.{}f}".format(waypoint.lat.value, writer.precisions["lat_lon"]))'
        if "lon" in fields:
            code += '\n\t\twriter.set_not_none(waypoint_, "lon", "{:.{}f}".format(waypoint.lon.value, writer.precisions["lat_lon"]))'
        if "ele" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "ele", waypoint.ele, writer.precisions["elevation"])'
        if "time" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_time(waypoint_, "time", waypoint.time, writer.time_format)'
        if "magvar" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "magvar", waypoint.magvar.value, writer.precisions["default"])'
        if "geoidheight" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "geoidheight", waypoint.geoidheight, writer.precisions["default"])'
        if "name" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "name", waypoint.name)'
        if "cmt" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "cmt", waypoint.cmt)'
        if "desc" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "desc", waypoint.desc)'
        if "src" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "src", waypoint.src)'
        if "link" in fields:
            code += "\n\t\tfor l in waypoint.link:"
            code += "\n\t\t\twaypoint_ = writer.add_link(waypoint_, l)"
        if "sym" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "sym", waypoint.sym)'
        if "type" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "type", waypoint.type)'
        if "fix" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "fix", waypoint.fix.value)'
        if "sat" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "sat", waypoint.sat, 0)'
        if "hdop" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "hdop", waypoint.hdop, writer.precisions["default"])'
        if "vdop" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "vdop", waypoint.vdop, writer.precisions["default"])'
        if "pdop" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "pdop", waypoint.pdop, writer.precisions["default"])'
        if "ageofdgpsdata" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "ageofdgpsdata", waypoint.ageofdgpsdata, writer.precisions["default"])'
        if "dgpsid" in fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "dgpsid", waypoint.dgpsid.value, 0)'
        if "extensions" in fields:
            # code += '\n\t\twaypoint_ = writer.add_trkpt_extensions(waypoint_, waypoint.extensions)'
            code += '\n\t\twaypoint_ = writer.add_extensions(waypoint_, waypoint.extensions, writer.extensions_fields.get("trkpt"))'
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_track_point>", "exec").co_consts[0],
            globals(),
            "_add_track_point",
        )
