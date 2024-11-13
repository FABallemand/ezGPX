
from typing import List
import xml.etree.ElementTree as ET
from types import FunctionType


class GPXWriterMethodBehaviorCreator():

    def __init__(self):
        pass

    def add_bounds_creator(self, bounds_fields):
        code = ('def _add_bound(writer, element, bounds):'
                '\n\tif bounds is not None:'
                '\n\t\tbounds_ = ET.SubElement(element, bounds.tag)')
        if "minlat" in bounds_fields:
            code += '\n\t\tbounds_, _ = writer.add_subelement_number(bounds_, "minlat", bounds.minlat, writer.precisions["lat_lon"])'
        if "minlon" in bounds_fields:
            code += '\n\t\tbounds_, _ = writer.add_subelement_number(bounds_, "minlon", bounds.minlon, writer.precisions["lat_lon"])'
        if "maxlat" in bounds_fields:
            code += '\n\t\tbounds_, _ = writer.add_subelement_number(bounds_, "maxlat", bounds.maxlat, writer.precisions["lat_lon"])'
        if "maxlon" in bounds_fields:
            code += '\n\t\tbounds_, _ = writer.add_subelement_number(bounds_, "maxlon", bounds.maxlon, writer.precisions["lat_lon"])'
        code += '\n\treturn element'
        compiled_code = compile(code, "<_add_bounds>", "exec")
        func = FunctionType(
            compiled_code.co_consts[0], globals(), "_add_bounds")
        return func

    def add_copyright_creator(self, copyright_fields):
        code = ('def _add_copyright(writer, element, copyright):'
                '\n\tif copyright is not None:'
                '\n\t\tcopyright_ = ET.SubElement(element, copyright.tag)')
        if "author" in copyright_fields:
            code += '\n\t\twriter.setIfNotNone(copyright_, "author", copyright.author)'
        if "year" in copyright_fields:
            code += '\n\t\tcopyright_, _ = writer.add_subelement(copyright_, "year", str(copyright.year))'
        if "licence" in copyright_fields:
            code += '\n\t\tcopyright_, _ = writer.add_subelement(copyright_, "licence", str(copyright.licence))'
        code += '\n\treturn element'
        compiled_code = compile(code, "<_add_copyright>", "exec")
        func = FunctionType(
            compiled_code.co_consts[0], globals(), "_add_copyright")
        return func

    def add_email_creator(self, email_fields):
        code = ('def _add_email(writer, element, email):'
                '\n\tif email is not None:'
                '\n\t\temail_ = ET.SubElement(element, email.tag)')
        if "id" in email_fields:
            code += '\n\t\twriter.setIfNotNone(email_, "id", email.id)'
        if "domain" in email_fields:
            code += '\n\t\twriter.setIfNotNone(email_, "domain", email.domain)'
        code += '\n\treturn element'
        compiled_code = compile(code, "<_add_email>", "exec")
        func = FunctionType(
            compiled_code.co_consts[0], globals(), "_add_email")
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
        code = ('def _add_link(writer, element, link):'
                '\n\tif link is not None:'
                '\n\t\tlink_ = ET.SubElement(element, link.tag)')
        if "href" in link_fields:
            code += ('\n\t\tif link.href is not None:'
                     '\n\t\t\twriter.setIfNotNone(link_, "href", link.href)')
        if "text" in link_fields:
            code += '\n\t\tlink_, _ = writer.add_subelement(link_, "text", link.text)'
        if "type" in link_fields:
            code += '\n\t\tlink_, _ = writer.add_subelement(link_, "type", link.type)'
        code += '\n\treturn element'
        compiled_code = compile(code, "<_add_link>", "exec")
        func = FunctionType(compiled_code.co_consts[0], globals(), "_add_link")
        return func

    def add_metadata_creator(self, metadata_fields: List[str]):
        code = ('def _add_metadata(writer, element, metadata):'
                '\n\tif metadata is not None:'
                '\n\t\tmetadata_ = ET.SubElement(element, metadata.tag)')
        if "name" in metadata_fields:
            code += '\n\t\tmetadata_, _ = writer.add_subelement(metadata_, "name", metadata.name)'
        if "desc" in metadata_fields:
            code += '\n\t\tmetadata_, _ = writer.add_subelement(metadata_, "desc", metadata.desc)'
        if "author" in metadata_fields:
            code += '\n\t\tmetadata_ = writer.add_person(metadata_, metadata.author)'
        if "copyright" in metadata_fields:
            code += '\n\t\tmetadata_ = writer.add_copyright(metadata_, metadata.copyright)'
        if "link" in metadata_fields:
            code += '\n\t\tmetadata_ = writer.add_link(metadata_, metadata.link)'
        if "time" in metadata_fields:
            code += '\n\t\tmetadata_, _ = writer.add_subelement_time(metadata_, "time", metadata.time, writer.time_format)'
        if "keywords" in metadata_fields:
            code += '\n\t\tmetadata_, _ = writer.add_subelement(metadata_, "keywords", metadata.keywords)'
        if "bounds" in metadata_fields:
            code += '\n\t\tmetadata_ = writer.add_bounds(metadata_, metadata.bounds)'
        if "extensions" in metadata_fields:
            # code += '\n\t\tmetadata_ = writer.add_metadata_extensions(metadata_, metadata.extensions)'
            code += '\n\t\tmetadata_ = writer.add_extensions(metadata_, metadata.extensions, writer.extensions_fields.get("metadata"))'
        code += '\n\treturn element'
        compiled_code = compile(code, "<_add_metadata>", "exec")
        func = FunctionType(
            compiled_code.co_consts[0], globals(), "_add_metadata")
        return func

    def add_person_creator(self, person_fields):
        code = ('def _add_person(writer, element, person):'
                '\n\tif person is not None:'
                '\n\t\tperson_ = ET.SubElement(element, person.tag)')
        if "name" in person_fields:
            code += '\n\t\tperson_, _ = writer.add_subelement(person_, "name", person.name)'
        if "email" in person_fields:
            code += '\n\t\tperson_ = writer.add_email(person_, person.email)'
        if "link" in person_fields:
            code += '\n\t\tperson_ = writer.add_link(person_, person.link)'
        code += '\n\treturn element'
        compiled_code = compile(code, "<_add_person>", "exec")
        func = FunctionType(
            compiled_code.co_consts[0], globals(), "_add_person")
        return func

    def add_point_segment_creator(self, point_segment_fields):
        code = ('def _add_point_segment(writer, element, point_segment):'
                '\n\tif point_segment is not None:'
                '\n\t\tpoint_segment_ = ET.SubElement(element, point_segment.tag)')
        if "pt" in point_segment_fields:
            code += ('\n\t\tfor point in point_segment.pt:'
                     '\n\t\t\tpoint_segment_ = writer.add_point(point_segment_, point)')
        code += '\n\treturn element'
        compiled_code = compile(code, "<_add_point_segment>", "exec")
        func = FunctionType(
            compiled_code.co_consts[0], globals(), "_add_point_segment")
        return func

    def add_point_creator(self, point_fields):
        code = ('def _add_point(writer, element, point):'
                '\n\tif point is not None:'
                '\n\t\tpoint_ = ET.SubElement(element, point.tag)')
        if "lat" in point_fields:
            code += '\n\t\twriter.setIfNotNone(point_, "lat", "{:.{}f}".format(point.lat, writer.precisions["lat_lon"]))'
        if "lon" in point_fields:
            code += '\n\t\twriter.setIfNotNone(point_, "lon", "{:.{}f}".format(point.lon, writer.precisions["lat_lon"]))'
        if "ele" in point_fields:
            code += '\n\t\tpoint_ = writer.add_subelement_number(point_, "ele", point.ele, writer.precisions["elevation"])'
        if "time" in point_fields:
            code += '\n\t\tpoint_, _ = writer.add_subelement_time(point_, "time", point.time, writer.time_format)'
        code += '\n\treturn element'
        compiled_code = compile(code, "<_add_point>", "exec")
        func = FunctionType(
            compiled_code.co_consts[0], globals(), "_add_point")
        return func

    def add_route_creator(self, route_fields):
        code = ('def _add_route(writer, element, route):'
                '\n\tif route is not None:'
                '\n\t\troute_ = ET.SubElement(element, route.tag)')
        if "name" in route_fields:
            code += '\n\t\troute_, _ = writer.add_subelement(route_, "name", route.name)'
        if "cmt" in route_fields:
            code += '\n\t\troute_, _ = writer.add_subelement(route_, "cmt", route.cmt)'
        if "desc" in route_fields:
            code += '\n\t\troute_, _ = writer.add_subelement(route_, "desc", route.desc)'
        if "src" in route_fields:
            code += '\n\t\troute_, _ = writer.add_subelement(route_, "src", route.src)'
        if "link" in route_fields:
            code += '\n\t\troute_ = writer.add_link(route_, route.link)'
        if "number" in route_fields:
            code += '\n\t\troute_, _ = writer.add_subelement_number(route_, "number", route.src, 0)'
        if "type" in route_fields:
            code += '\n\t\troute_, _ = writer.add_subelement(route_, "type", route.type)'
        if "extensions" in route_fields:
            # code += '\n\t\troute_ = writer.add_rte_extensions(route_, route.extensions)'
            code += '\n\t\troute_ = writer.add_extensions(route_, route.extensions, writer.extensions_fields.get("rte"))'
        if "rtept" in route_fields:
            code += ('\n\t\tfor way_point in route.rtept:'
                     '\n\t\t\troute_ = writer.add_way_point(route_, way_point)')
        code += '\n\treturn element'
        compiled_code = compile(code, "<_add_route>", "exec")
        func = FunctionType(
            compiled_code.co_consts[0], globals(), "_add_route")
        return func

    def add_track_segment_creator(self, track_segment_fields):
        code = ('def _add_track_segment(writer, element, track_segment):'
                '\n\tif track_segment is not None:'
                '\n\t\ttrack_segment_ = ET.SubElement(element, track_segment.tag)')
        if "extensions" in track_segment_fields:
            # code += '\n\t\ttrack_segment_ = writer.add_trkseg_extensions(track_segment_, track_segment.extensions)'
            code += '\n\t\ttrack_segment_ = writer.add_extensions(track_segment_, track_segment.extensions, writer.extensions_fields.get("trkseg"))'
        if "trkpt" in track_segment_fields:
            code += ('\n\t\tfor track_point in track_segment.trkpt:'
                     '\n\t\t\ttrack_segment_ = writer.add_track_point(track_segment_, track_point)')
        code += '\n\treturn element'
        compiled_code = compile(code, "<_add_track_segment>", "exec")
        func = FunctionType(
            compiled_code.co_consts[0], globals(), "_add_track_segment")
        return func

    def add_track_creator(self, track_fields):
        code = ('def _add_track(writer, element, track):'
                '\n\tif track is not None:'
                '\n\t\ttrack_ = ET.SubElement(element, track.tag)')
        if "name" in track_fields:
            code += '\n\t\ttrack_, _ = writer.add_subelement(track_, "name", track.name)'
        if "cmt" in track_fields:
            code += '\n\t\ttrack_, _ = writer.add_subelement(track_, "cmt", track.cmt)'
        if "desc" in track_fields:
            code += '\n\t\ttrack_, _ = writer.add_subelement(track_, "desc", track.desc)'
        if "src" in track_fields:
            code += '\n\t\ttrack_, _ = writer.add_subelement(track_, "src", track.src)'
        if "link" in track_fields:
            code += '\n\t\ttrack_ = writer.add_link(track_, track.link)'
        if "number" in track_fields:
            code += '\n\t\ttrack_, _ = writer.add_subelement_number(track_, "number", track.src, 0)'
        if "type" in track_fields:
            code += '\n\t\ttrack_, _ = writer.add_subelement(track_, "type", track.type)'
        if "extensions" in track_fields:
            # code += '\n\t\ttrack_ = writer.add_trk_extensions(track_, track.extensions)'
            code += '\n\t\ttrack_ = writer.add_extensions(track_, track.extensions, writer.extensions_fields.get("trk"))'
        if "trkseg" in track_fields:
            code += ('\n\t\tfor track_seg in track.trkseg:'
                     '\n\t\t\ttrack_ = writer.add_track_segment(track_, track_seg)')
        code += '\n\treturn element'
        compiled_code = compile(code, "<_add_track>", "exec")
        func = FunctionType(
            compiled_code.co_consts[0], globals(), "_add_track")
        return func

    def add_way_point_creator(self, way_point_fields):
        code = ('def _add_way_point(writer, element, way_point):'
                '\n\tif way_point is not None:'
                '\n\t\tway_point_ = ET.SubElement(element, way_point.tag)')
        if "lat" in way_point_fields:
            code += '\n\t\twriter.setIfNotNone(way_point_, "lat", "{:.{}f}".format(way_point.lat, writer.precisions["lat_lon"]))'
        if "lon" in way_point_fields:
            code += '\n\t\twriter.setIfNotNone(way_point_, "lon", "{:.{}f}".format(way_point.lon, writer.precisions["lat_lon"]))'
        if "ele" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "ele", way_point.ele, writer.precisions["elevation"])'
        if "time" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_time(way_point_, "time", way_point.time, writer.time_format)'
        if "magvar" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "magvar", way_point.mag_var, writer.precisions["default"])'
        if "geoidheight" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "geoidheight", way_point.geo_id_height, writer.precisions["default"])'
        if "name" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement(way_point_, "name", way_point.name)'
        if "cmt" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement(way_point_, "cmt", way_point.cmt)'
        if "desc" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement(way_point_, "desc", way_point.desc)'
        if "src" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement(way_point_, "src", way_point.src)'
        if "link" in way_point_fields:
            code += '\n\t\tway_point_ = writer.add_link(way_point_, way_point.link)'
        if "sym" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement(way_point_, "sym", way_point.sym)'
        if "type" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement(way_point_, "type", way_point.type)'
        if "fix" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement(way_point_, "fix", way_point.fix)'
        if "sat" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "sat", way_point.sat, 0)'
        if "hdop" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "hdop", way_point.hdop, writer.precisions["default"])'
        if "vdop" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "vdop", way_point.vdop, writer.precisions["default"])'
        if "pdop" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "pdop", way_point.pdop, writer.precisions["default"])'
        if "ageofgpsdata" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "ageofgpsdata", way_point.age_of_gps_data, writer.precisions["default"])'
        if "dgpsid" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "dgpsid", way_point.dgpsid, 0)'
        if "extensions" in way_point_fields:
            # code += '\n\t\tway_point_ = writer.add_wpt_extensions(way_point_, way_point.extensions)'
            code += '\n\t\tway_point_ = writer.add_extensions(way_point_, way_point.extensions, writer.extensions_fields.get("wpt"))'
        code += '\n\treturn element'
        compiled_code = compile(code, "<_add_way_point>", "exec")
        func = FunctionType(
            compiled_code.co_consts[0], globals(), "_add_way_point")
        return func

    def add_track_point_creator(self, way_point_fields):
        code = ('def _add_track_point(writer, element, way_point):'
                '\n\tif way_point is not None:'
                '\n\t\tway_point_ = ET.SubElement(element, way_point.tag)')
        if "lat" in way_point_fields:
            code += '\n\t\twriter.setIfNotNone(way_point_, "lat", "{:.{}f}".format(way_point.lat, writer.precisions["lat_lon"]))'
        if "lon" in way_point_fields:
            code += '\n\t\twriter.setIfNotNone(way_point_, "lon", "{:.{}f}".format(way_point.lon, writer.precisions["lat_lon"]))'
        if "ele" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "ele", way_point.ele, writer.precisions["elevation"])'
        if "time" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_time(way_point_, "time", way_point.time, writer.time_format)'
        if "magvar" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "magvar", way_point.mag_var, writer.precisions["default"])'
        if "geoidheight" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "geoidheight", way_point.geo_id_height, writer.precisions["default"])'
        if "name" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement(way_point_, "name", way_point.name)'
        if "cmt" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement(way_point_, "cmt", way_point.cmt)'
        if "desc" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement(way_point_, "desc", way_point.desc)'
        if "src" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement(way_point_, "src", way_point.src)'
        if "link" in way_point_fields:
            code += '\n\t\tway_point_ = writer.add_link(way_point_, way_point.link)'
        if "sym" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement(way_point_, "sym", way_point.sym)'
        if "type" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement(way_point_, "type", way_point.type)'
        if "fix" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement(way_point_, "fix", way_point.fix)'
        if "sat" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "sat", way_point.sat, 0)'
        if "hdop" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "hdop", way_point.hdop, writer.precisions["default"])'
        if "vdop" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "vdop", way_point.vdop, writer.precisions["default"])'
        if "pdop" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "pdop", way_point.pdop, writer.precisions["default"])'
        if "ageofgpsdata" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "ageofgpsdata", way_point.age_of_gps_data, writer.precisions["default"])'
        if "dgpsid" in way_point_fields:
            code += '\n\t\tway_point_, _ = writer.add_subelement_number(way_point_, "dgpsid", way_point.dgpsid, 0)'
        if "extensions" in way_point_fields:
            # code += '\n\t\tway_point_ = writer.add_trkpt_extensions(way_point_, way_point.extensions)'
            code += '\n\t\tway_point_ = writer.add_extensions(way_point_, way_point.extensions, writer.extensions_fields.get("trkpt"))'
        code += '\n\treturn element'
        compiled_code = compile(code, "<_add_track_point>", "exec")
        func = FunctionType(
            compiled_code.co_consts[0], globals(), "_add_track_point")
        return func
