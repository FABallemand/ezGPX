# ruff: noqa: F401
"""
This module contains the GPXWriterMethodCreator class.
"""

import xml.etree.ElementTree as ET  # pylint: disable=unused-import
from types import FunctionType


class GPXWriterMethodCreator:
    """
    GPXWriter method creator.
    """

    def add_bounds_creator(self, bounds_fields):
        code = (
            "def _add_bound(writer, element, bounds):"
            "\n\tif bounds is not None:"
            "\n\t\tbounds_ = ET.SubElement(element, bounds.tag)"
        )
        if "minlat" in bounds_fields:
            code += '\n\t\tbounds_, _ = writer.add_subelement_number(bounds_, "minlat", bounds.minlat, writer.precisions["lat_lon"])'
        if "minlon" in bounds_fields:
            code += '\n\t\tbounds_, _ = writer.add_subelement_number(bounds_, "minlon", bounds.minlon, writer.precisions["lat_lon"])'
        if "maxlat" in bounds_fields:
            code += '\n\t\tbounds_, _ = writer.add_subelement_number(bounds_, "maxlat", bounds.maxlat, writer.precisions["lat_lon"])'
        if "maxlon" in bounds_fields:
            code += '\n\t\tbounds_, _ = writer.add_subelement_number(bounds_, "maxlon", bounds.maxlon, writer.precisions["lat_lon"])'
        code += "\n\treturn element"
        compiled_code = compile(code, "<_add_bounds>", "exec")
        func = FunctionType(compiled_code.co_consts[0], globals(), "_add_bounds")
        return func

    def add_copyright_creator(self, copyright_fields):
        code = (
            "def _add_copyright(writer, element, copyright):"
            "\n\tif copyright is not None:"
            "\n\t\tcopyright_ = ET.SubElement(element, copyright.tag)"
        )
        if "author" in copyright_fields:
            code += '\n\t\twriter.set_not_none(copyright_, "author", copyright.author)'
        if "year" in copyright_fields:
            code += '\n\t\tcopyright_, _ = writer.add_subelement(copyright_, "year", str(copyright.year))'
        if "licence" in copyright_fields:
            code += '\n\t\tcopyright_, _ = writer.add_subelement(copyright_, "licence", str(copyright.licence))'
        code += "\n\treturn element"
        compiled_code = compile(code, "<_add_copyright>", "exec")
        func = FunctionType(compiled_code.co_consts[0], globals(), "_add_copyright")
        return func

    def add_email_creator(self, email_fields):
        code = (
            "def _add_email(writer, element, email):"
            "\n\tif email is not None:"
            "\n\t\temail_ = ET.SubElement(element, email.tag)"
        )
        if "id" in email_fields:
            code += '\n\t\twriter.set_not_none(email_, "id", email.id)'
        if "domain" in email_fields:
            code += '\n\t\twriter.set_not_none(email_, "domain", email.domain)'
        code += "\n\treturn element"
        compiled_code = compile(code, "<_add_email>", "exec")
        func = FunctionType(compiled_code.co_consts[0], globals(), "_add_email")
        return func

    # def add_extensions_creator(self, extensions_fields):
    #     code = ('def _add_extensions(writer, element, extensions):'
    #             '\n\tif extensions is not None:'
    #             '\n\t\textensions_ = ET.SubElement(element, extensions.tag)')
    #     if extensions_fields is not None:
    #         for k, v in extensions_fields:
    #             code += f'\n\t\textensions_, _ = writer.add_extensions_element(extensions_, "{k}", extensions.values["{field}"])'
    #     code += '\n\treturn element'
    #     compiled_code = compile(code, "<_add_extensions>", "exec")
    #     func = FunctionType(compiled_code.co_consts[0], globals(), "_add_extensions")
    #     return func

    def add_link_creator(self, link_fields):
        code = (
            "def _add_link(writer, element, link):"
            "\n\tif link is not None:"
            "\n\t\tlink_ = ET.SubElement(element, link.tag)"
        )
        if "href" in link_fields:
            code += (
                "\n\t\tif link.href is not None:"
                '\n\t\t\twriter.set_not_none(link_, "href", link.href)'
            )
        if "text" in link_fields:
            code += '\n\t\tlink_, _ = writer.add_subelement(link_, "text", link.text)'
        if "type" in link_fields:
            code += '\n\t\tlink_, _ = writer.add_subelement(link_, "type", link.type)'
        code += "\n\treturn element"
        compiled_code = compile(code, "<_add_link>", "exec")
        func = FunctionType(compiled_code.co_consts[0], globals(), "_add_link")
        return func

    def add_metadata_creator(self, metadata_fields: list[str]):
        code = (
            "def _add_metadata(writer, element, metadata):"
            "\n\tif metadata is not None:"
            "\n\t\tmetadata_ = ET.SubElement(element, metadata.tag)"
        )
        if "name" in metadata_fields:
            code += '\n\t\tmetadata_, _ = writer.add_subelement(metadata_, "name", metadata.name)'
        if "desc" in metadata_fields:
            code += '\n\t\tmetadata_, _ = writer.add_subelement(metadata_, "desc", metadata.desc)'
        if "author" in metadata_fields:
            code += "\n\t\tmetadata_ = writer.add_person(metadata_, metadata.author)"
        if "copyright" in metadata_fields:
            code += (
                "\n\t\tmetadata_ = writer.add_copyright(metadata_, metadata.copyright)"
            )
        if "link" in metadata_fields:
            code += "\n\t\tmetadata_ = writer.add_link(metadata_, metadata.link)"
        if "time" in metadata_fields:
            code += '\n\t\tmetadata_, _ = writer.add_subelement_time(metadata_, "time", metadata.time, writer.time_format)'
        if "keywords" in metadata_fields:
            code += '\n\t\tmetadata_, _ = writer.add_subelement(metadata_, "keywords", metadata.keywords)'
        if "bounds" in metadata_fields:
            code += "\n\t\tmetadata_ = writer.add_bounds(metadata_, metadata.bounds)"
        if "extensions" in metadata_fields:
            # code += '\n\t\tmetadata_ = writer.add_metadata_extensions(metadata_, metadata.extensions)'
            code += '\n\t\tmetadata_ = writer.add_extensions(metadata_, metadata.extensions, writer.extensions_fields.get("metadata"))'
        code += "\n\treturn element"
        compiled_code = compile(code, "<_add_metadata>", "exec")
        func = FunctionType(compiled_code.co_consts[0], globals(), "_add_metadata")
        return func

    def add_person_creator(self, person_fields):
        code = (
            "def _add_person(writer, element, person):"
            "\n\tif person is not None:"
            "\n\t\tperson_ = ET.SubElement(element, person.tag)"
        )
        if "name" in person_fields:
            code += (
                '\n\t\tperson_, _ = writer.add_subelement(person_, "name", person.name)'
            )
        if "email" in person_fields:
            code += "\n\t\tperson_ = writer.add_email(person_, person.email)"
        if "link" in person_fields:
            code += "\n\t\tperson_ = writer.add_link(person_, person.link)"
        code += "\n\treturn element"
        compiled_code = compile(code, "<_add_person>", "exec")
        func = FunctionType(compiled_code.co_consts[0], globals(), "_add_person")
        return func

    def add_point_segment_creator(self, point_segment_fields):
        code = (
            "def _add_point_segment(writer, element, point_segment):"
            "\n\tif point_segment is not None:"
            "\n\t\tpoint_segment_ = ET.SubElement(element, point_segment.tag)"
        )
        if "pt" in point_segment_fields:
            code += (
                "\n\t\tfor point in point_segment.pt:"
                "\n\t\t\tpoint_segment_ = writer.add_point(point_segment_, point)"
            )
        code += "\n\treturn element"
        compiled_code = compile(code, "<_add_point_segment>", "exec")
        func = FunctionType(compiled_code.co_consts[0], globals(), "_add_point_segment")
        return func

    def add_point_creator(self, point_fields):
        code = (
            "def _add_point(writer, element, point):"
            "\n\tif point is not None:"
            "\n\t\tpoint_ = ET.SubElement(element, point.tag)"
        )
        if "lat" in point_fields:
            code += '\n\t\twriter.set_not_none(point_, "lat", "{:.{}f}".format(point.lat, writer.precisions["lat_lon"]))'
        if "lon" in point_fields:
            code += '\n\t\twriter.set_not_none(point_, "lon", "{:.{}f}".format(point.lon, writer.precisions["lat_lon"]))'
        if "ele" in point_fields:
            code += '\n\t\tpoint_ = writer.add_subelement_number(point_, "ele", point.ele, writer.precisions["elevation"])'
        if "time" in point_fields:
            code += '\n\t\tpoint_, _ = writer.add_subelement_time(point_, "time", point.time, writer.time_format)'
        code += "\n\treturn element"
        compiled_code = compile(code, "<_add_point>", "exec")
        func = FunctionType(compiled_code.co_consts[0], globals(), "_add_point")
        return func

    def add_route_creator(self, route_fields):
        code = (
            "def _add_route(writer, element, route):"
            "\n\tif route is not None:"
            "\n\t\troute_ = ET.SubElement(element, route.tag)"
        )
        if "name" in route_fields:
            code += (
                '\n\t\troute_, _ = writer.add_subelement(route_, "name", route.name)'
            )
        if "cmt" in route_fields:
            code += '\n\t\troute_, _ = writer.add_subelement(route_, "cmt", route.cmt)'
        if "desc" in route_fields:
            code += (
                '\n\t\troute_, _ = writer.add_subelement(route_, "desc", route.desc)'
            )
        if "src" in route_fields:
            code += '\n\t\troute_, _ = writer.add_subelement(route_, "src", route.src)'
        if "link" in route_fields:
            code += "\n\t\troute_ = writer.add_link(route_, route.link)"
        if "number" in route_fields:
            code += '\n\t\troute_, _ = writer.add_subelement_number(route_, "number", route.src, 0)'
        if "type" in route_fields:
            code += (
                '\n\t\troute_, _ = writer.add_subelement(route_, "type", route.type)'
            )
        if "extensions" in route_fields:
            # code += '\n\t\troute_ = writer.add_rte_extensions(route_, route.extensions)'
            code += '\n\t\troute_ = writer.add_extensions(route_, route.extensions, writer.extensions_fields.get("rte"))'
        if "rtept" in route_fields:
            code += (
                "\n\t\tfor waypoint in route.rtept:"
                "\n\t\t\troute_ = writer.add_waypoint(route_, waypoint)"
            )
        code += "\n\treturn element"
        compiled_code = compile(code, "<_add_route>", "exec")
        func = FunctionType(compiled_code.co_consts[0], globals(), "_add_route")
        return func

    def add_track_segment_creator(self, track_segment_fields):
        code = (
            "def _add_track_segment(writer, element, track_segment):"
            "\n\tif track_segment is not None:"
            "\n\t\ttrack_segment_ = ET.SubElement(element, track_segment.tag)"
        )
        if "extensions" in track_segment_fields:
            # code += '\n\t\ttrack_segment_ = writer.add_trkseg_extensions(track_segment_, track_segment.extensions)'
            code += '\n\t\ttrack_segment_ = writer.add_extensions(track_segment_, track_segment.extensions, writer.extensions_fields.get("trkseg"))'
        if "trkpt" in track_segment_fields:
            code += (
                "\n\t\tfor track_point in track_segment.trkpt:"
                "\n\t\t\ttrack_segment_ = writer.add_track_point(track_segment_, track_point)"
            )
        code += "\n\treturn element"
        compiled_code = compile(code, "<_add_track_segment>", "exec")
        func = FunctionType(compiled_code.co_consts[0], globals(), "_add_track_segment")
        return func

    def add_track_creator(self, track_fields):
        code = (
            "def _add_track(writer, element, track):"
            "\n\tif track is not None:"
            "\n\t\ttrack_ = ET.SubElement(element, track.tag)"
        )
        if "name" in track_fields:
            code += (
                '\n\t\ttrack_, _ = writer.add_subelement(track_, "name", track.name)'
            )
        if "cmt" in track_fields:
            code += '\n\t\ttrack_, _ = writer.add_subelement(track_, "cmt", track.cmt)'
        if "desc" in track_fields:
            code += (
                '\n\t\ttrack_, _ = writer.add_subelement(track_, "desc", track.desc)'
            )
        if "src" in track_fields:
            code += '\n\t\ttrack_, _ = writer.add_subelement(track_, "src", track.src)'
        if "link" in track_fields:
            code += "\n\t\ttrack_ = writer.add_link(track_, track.link)"
        if "number" in track_fields:
            code += '\n\t\ttrack_, _ = writer.add_subelement_number(track_, "number", track.src, 0)'
        if "type" in track_fields:
            code += (
                '\n\t\ttrack_, _ = writer.add_subelement(track_, "type", track.type)'
            )
        if "extensions" in track_fields:
            # code += '\n\t\ttrack_ = writer.add_trk_extensions(track_, track.extensions)'
            code += '\n\t\ttrack_ = writer.add_extensions(track_, track.extensions, writer.extensions_fields.get("trk"))'
        if "trkseg" in track_fields:
            code += (
                "\n\t\tfor track_seg in track.trkseg:"
                "\n\t\t\ttrack_ = writer.add_track_segment(track_, track_seg)"
            )
        code += "\n\treturn element"
        compiled_code = compile(code, "<_add_track>", "exec")
        func = FunctionType(compiled_code.co_consts[0], globals(), "_add_track")
        return func

    def add_waypoint_creator(self, waypoint_fields):
        code = (
            "def _add_waypoint(writer, element, waypoint):"
            "\n\tif waypoint is not None:"
            "\n\t\twaypoint_ = ET.SubElement(element, waypoint.tag)"
        )
        if "lat" in waypoint_fields:
            code += '\n\t\twriter.set_not_none(waypoint_, "lat", "{:.{}f}".format(waypoint.lat, writer.precisions["lat_lon"]))'
        if "lon" in waypoint_fields:
            code += '\n\t\twriter.set_not_none(waypoint_, "lon", "{:.{}f}".format(waypoint.lon, writer.precisions["lat_lon"]))'
        if "ele" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "ele", waypoint.ele, writer.precisions["elevation"])'
        if "time" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_time(waypoint_, "time", waypoint.time, writer.time_format)'
        if "magvar" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "magvar", waypoint.mag_var, writer.precisions["default"])'
        if "geoidheight" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "geoidheight", waypoint.geo_id_height, writer.precisions["default"])'
        if "name" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "name", waypoint.name)'
        if "cmt" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "cmt", waypoint.cmt)'
        if "desc" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "desc", waypoint.desc)'
        if "src" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "src", waypoint.src)'
        if "link" in waypoint_fields:
            code += "\n\t\twaypoint_ = writer.add_link(waypoint_, waypoint.link)"
        if "sym" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "sym", waypoint.sym)'
        if "type" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "type", waypoint.type)'
        if "fix" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "fix", waypoint.fix)'
        if "sat" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "sat", waypoint.sat, 0)'
        if "hdop" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "hdop", waypoint.hdop, writer.precisions["default"])'
        if "vdop" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "vdop", waypoint.vdop, writer.precisions["default"])'
        if "pdop" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "pdop", waypoint.pdop, writer.precisions["default"])'
        if "ageofgpsdata" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "ageofgpsdata", waypoint.age_of_gps_data, writer.precisions["default"])'
        if "dgpsid" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "dgpsid", waypoint.dgpsid, 0)'
        if "extensions" in waypoint_fields:
            # code += '\n\t\twaypoint_ = writer.add_wpt_extensions(waypoint_, waypoint.extensions)'
            code += '\n\t\twaypoint_ = writer.add_extensions(waypoint_, waypoint.extensions, writer.extensions_fields.get("wpt"))'
        code += "\n\treturn element"
        compiled_code = compile(code, "<_add_waypoint>", "exec")
        func = FunctionType(compiled_code.co_consts[0], globals(), "_add_waypoint")
        return func

    def add_track_point_creator(self, waypoint_fields):
        code = (
            "def _add_track_point(writer, element, waypoint):"
            "\n\tif waypoint is not None:"
            "\n\t\twaypoint_ = ET.SubElement(element, waypoint.tag)"
        )
        if "lat" in waypoint_fields:
            code += '\n\t\twriter.set_not_none(waypoint_, "lat", "{:.{}f}".format(waypoint.lat, writer.precisions["lat_lon"]))'
        if "lon" in waypoint_fields:
            code += '\n\t\twriter.set_not_none(waypoint_, "lon", "{:.{}f}".format(waypoint.lon, writer.precisions["lat_lon"]))'
        if "ele" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "ele", waypoint.ele, writer.precisions["elevation"])'
        if "time" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_time(waypoint_, "time", waypoint.time, writer.time_format)'
        if "magvar" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "magvar", waypoint.mag_var, writer.precisions["default"])'
        if "geoidheight" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "geoidheight", waypoint.geo_id_height, writer.precisions["default"])'
        if "name" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "name", waypoint.name)'
        if "cmt" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "cmt", waypoint.cmt)'
        if "desc" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "desc", waypoint.desc)'
        if "src" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "src", waypoint.src)'
        if "link" in waypoint_fields:
            code += "\n\t\twaypoint_ = writer.add_link(waypoint_, waypoint.link)"
        if "sym" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "sym", waypoint.sym)'
        if "type" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "type", waypoint.type)'
        if "fix" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement(waypoint_, "fix", waypoint.fix)'
        if "sat" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "sat", waypoint.sat, 0)'
        if "hdop" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "hdop", waypoint.hdop, writer.precisions["default"])'
        if "vdop" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "vdop", waypoint.vdop, writer.precisions["default"])'
        if "pdop" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "pdop", waypoint.pdop, writer.precisions["default"])'
        if "ageofgpsdata" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "ageofgpsdata", waypoint.age_of_gps_data, writer.precisions["default"])'
        if "dgpsid" in waypoint_fields:
            code += '\n\t\twaypoint_, _ = writer.add_subelement_number(waypoint_, "dgpsid", waypoint.dgpsid, 0)'
        if "extensions" in waypoint_fields:
            # code += '\n\t\twaypoint_ = writer.add_trkpt_extensions(waypoint_, waypoint.extensions)'
            code += '\n\t\twaypoint_ = writer.add_extensions(waypoint_, waypoint.extensions, writer.extensions_fields.get("trkpt"))'
        code += "\n\treturn element"
        compiled_code = compile(code, "<_add_track_point>", "exec")
        func = FunctionType(compiled_code.co_consts[0], globals(), "_add_track_point")
        return func
