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

    def add_ptseg_creator(self, fields: list) -> FunctionType:
        """
        Create `add_ptseg` method.

        Args:
            fields (list): `Ptseg` fields.

        Returns:
            FunctionType: `add_ptseg` method.
        """
        code = (
            "def _add_ptseg(writer, element, ptseg):"
            "\n\tif ptseg is not None:"
            "\n\t\tptseg_ = ET.SubElement(element, ptseg.tag)"
        )
        if "pt" in fields:
            code += (
                "\n\t\tfor pt in ptseg.pt:\n\t\t\tptseg_ = writer.add_pt(ptseg_, pt)"
            )
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_ptseg>", "exec").co_consts[0],
            globals(),
            "_add_ptseg",
        )

    def add_pt_creator(self, fields: list) -> FunctionType:
        """
        Create `add_pt` method.

        Args:
            fields (list): `Pt` fields.

        Returns:
            FunctionType: `add_pt` method.
        """
        code = (
            "def _add_pt(writer, element, pt):"
            "\n\tif pt is not None:"
            "\n\t\tpt_ = ET.SubElement(element, pt.tag)"
        )
        if "lat" in fields:
            code += '\n\t\twriter.set_not_none(pt_, "lat", "{:.{}f}".format(pt.lat.value, writer.precisions["lat_lon"]))'
        if "lon" in fields:
            code += '\n\t\twriter.set_not_none(pt_, "lon", "{:.{}f}".format(pt.lon.value, writer.precisions["lat_lon"]))'
        if "ele" in fields:
            code += '\n\t\tpt_ = writer.add_subelement_number(pt_, "ele", pt.ele, writer.precisions["elevation"])'
        if "time" in fields:
            code += '\n\t\tpt_, _ = writer.add_subelement_time(pt_, "time", pt.time, writer.time_format)'
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_pt>", "exec").co_consts[0], globals(), "_add_pt"
        )

    def add_rte_creator(self, fields: list) -> FunctionType:
        """
        Create `add_rte` method.

        Args:
            fields (list): `Rte` fields.

        Returns:
            FunctionType: `add_rte` method.
        """
        code = (
            "def _add_rte(writer, element, rte):"
            "\n\tif rte is not None:"
            "\n\t\trte_ = ET.SubElement(element, rte.tag)"
        )
        if "name" in fields:
            code += '\n\t\trte_, _ = writer.add_subelement(rte_, "name", rte.name)'
        if "cmt" in fields:
            code += '\n\t\trte_, _ = writer.add_subelement(rte_, "cmt", rte.cmt)'
        if "desc" in fields:
            code += '\n\t\trte_, _ = writer.add_subelement(rte_, "desc", rte.desc)'
        if "src" in fields:
            code += '\n\t\trte_, _ = writer.add_subelement(rte_, "src", rte.src)'
        if "link" in fields:
            code += "\n\t\tfor l in rte.link:"
            code += "\n\t\t\trte_ = writer.add_link(rte_, l)"
        if "number" in fields:
            code += '\n\t\trte_, _ = writer.add_subelement_number(rte_, "number", rte.number)'
        if "type" in fields:
            code += '\n\t\trte_, _ = writer.add_subelement(rte_, "type", rte.type)'
        if "extensions" in fields:
            # code += '\n\t\trte_ = writer.add_rte_extensions(rte_, rte.extensions)'
            code += '\n\t\trte_ = writer.add_extensions(rte_, rte.extensions, writer.extensions_fields.get("rte"))'
        if "rtept" in fields:
            code += (
                "\n\t\tfor wpt in rte.rtept:\n\t\t\trte_ = writer.add_wpt(rte_, wpt)"
            )
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_rte>", "exec").co_consts[0], globals(), "_add_rte"
        )

    def add_trkseg_creator(self, fields: list) -> FunctionType:
        """
        Create `add_trkseg` method.

        Args:
            fields (list): `Trkseg` fields.

        Returns:
            FunctionType: `add_trkseg` method.
        """
        code = (
            "def _add_trkseg(writer, element, trkseg):"
            "\n\tif trkseg is not None:"
            "\n\t\ttrkseg_ = ET.SubElement(element, trkseg.tag)"
        )
        if "extensions" in fields:
            # code += '\n\t\ttrkseg_ = writer.add_trkseg_extensions(trkseg_, trkseg.extensions)'
            code += '\n\t\ttrkseg_ = writer.add_extensions(trkseg_, trkseg.extensions, writer.extensions_fields.get("trkseg"))'
        if "trkpt" in fields:
            code += (
                "\n\t\tfor trkpt in trkseg.trkpt:"
                "\n\t\t\ttrkseg_ = writer.add_trkpt(trkseg_, trkpt)"
            )
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_trkseg>", "exec").co_consts[0],
            globals(),
            "_add_trkseg",
        )

    def add_trk_creator(self, fields: list) -> FunctionType:
        """
        Create `add_trk` method.

        Args:
            fields (list): `Trk` fields.

        Returns:
            FunctionType: `add_trk` method.
        """
        code = (
            "def _add_trk(writer, element, trk):"
            "\n\tif trk is not None:"
            "\n\t\ttrk_ = ET.SubElement(element, trk.tag)"
        )
        if "name" in fields:
            code += '\n\t\ttrk_, _ = writer.add_subelement(trk_, "name", trk.name)'
        if "cmt" in fields:
            code += '\n\t\ttrk_, _ = writer.add_subelement(trk_, "cmt", trk.cmt)'
        if "desc" in fields:
            code += '\n\t\ttrk_, _ = writer.add_subelement(trk_, "desc", trk.desc)'
        if "src" in fields:
            code += '\n\t\ttrk_, _ = writer.add_subelement(trk_, "src", trk.src)'
        if "link" in fields:
            code += "\n\t\tfor l in trk.link:"
            code += "\n\t\t\ttrk_ = writer.add_link(trk_, l)"
        if "number" in fields:
            code += '\n\t\ttrk_, _ = writer.add_subelement_number(trk_, "number", trk.number)'
        if "type" in fields:
            code += '\n\t\ttrk_, _ = writer.add_subelement(trk_, "type", trk.type)'
        if "extensions" in fields:
            # code += '\n\t\ttrk_ = writer.add_trk_extensions(trk_, trk.extensions)'
            code += '\n\t\ttrk_ = writer.add_extensions(trk_, trk.extensions, writer.extensions_fields.get("trk"))'
        if "trkseg" in fields:
            code += (
                "\n\t\tfor trk_seg in trk.trkseg:"
                "\n\t\t\ttrk_ = writer.add_trkseg(trk_, trk_seg)"
            )
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_trk>", "exec").co_consts[0], globals(), "_add_trk"
        )

    def add_wpt_creator(self, fields: list) -> FunctionType:
        """
        Create `add_wpt` method.

        Args:
            fields (list): `Wpt` fields.

        Returns:
            FunctionType: `add_wpt` method.
        """
        code = (
            "def _add_wpt(writer, element, wpt):"
            "\n\tif wpt is not None:"
            "\n\t\twpt_ = ET.SubElement(element, wpt.tag)"
        )
        if "lat" in fields:
            code += '\n\t\twriter.set_not_none(wpt_, "lat", "{:.{}f}".format(wpt.lat.value, writer.precisions["lat_lon"]))'
        if "lon" in fields:
            code += '\n\t\twriter.set_not_none(wpt_, "lon", "{:.{}f}".format(wpt.lon.value, writer.precisions["lat_lon"]))'
        if "ele" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "ele", wpt.ele, writer.precisions["elevation"])'
        if "time" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_time(wpt_, "time", wpt.time, writer.time_format)'
        if "magvar" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "magvar", writer.get_value(wpt.magvar), writer.precisions["default"])'
        if "geoidheight" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "geoidheight", wpt.geoidheight, writer.precisions["default"])'
        if "name" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement(wpt_, "name", wpt.name)'
        if "cmt" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement(wpt_, "cmt", wpt.cmt)'
        if "desc" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement(wpt_, "desc", wpt.desc)'
        if "src" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement(wpt_, "src", wpt.src)'
        if "link" in fields:
            code += "\n\t\tfor l in wpt.link:"
            code += "\n\t\t\twpt_ = writer.add_link(wpt_, l)"
        if "sym" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement(wpt_, "sym", wpt.sym)'
        if "type" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement(wpt_, "type", wpt.type)'
        if "fix" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement(wpt_, "fix", writer.get_value(wpt.fix))'
        if "sat" in fields:
            code += (
                '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "sat", wpt.sat, 0)'
            )
        if "hdop" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "hdop", wpt.hdop, writer.precisions["default"])'
        if "vdop" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "vdop", wpt.vdop, writer.precisions["default"])'
        if "pdop" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "pdop", wpt.pdop, writer.precisions["default"])'
        if "ageofdgpsdata" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "ageofdgpsdata", wpt.ageofdgpsdata, writer.precisions["default"])'
        if "dgpsid" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "dgpsid", writer.get_value(wpt.dgpsid), 0)'
        if "extensions" in fields:
            # code += '\n\t\twpt_ = writer.add_wpt_extensions(wpt_, wpt.extensions)'
            code += '\n\t\twpt_ = writer.add_extensions(wpt_, wpt.extensions, writer.extensions_fields.get("wpt"))'
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_wpt>", "exec").co_consts[0],
            globals(),
            "_add_wpt",
        )

    def add_trkpt_creator(self, fields: list) -> FunctionType:
        """
        Create `add_wpt` method.

        Args:
            fields (list): `Wpt` fields.

        Returns:
            FunctionType: `add_wpt` method.
        """
        code = (
            "def _add_trkpt(writer, element, wpt):"
            "\n\tif wpt is not None:"
            "\n\t\twpt_ = ET.SubElement(element, wpt.tag)"
        )
        if "lat" in fields:
            code += '\n\t\twriter.set_not_none(wpt_, "lat", "{:.{}f}".format(wpt.lat.value, writer.precisions["lat_lon"]))'
        if "lon" in fields:
            code += '\n\t\twriter.set_not_none(wpt_, "lon", "{:.{}f}".format(wpt.lon.value, writer.precisions["lat_lon"]))'
        if "ele" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "ele", wpt.ele, writer.precisions["elevation"])'
        if "time" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_time(wpt_, "time", wpt.time, writer.time_format)'
        if "magvar" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "magvar", writer.get_value(wpt.magvar), writer.precisions["default"])'
        if "geoidheight" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "geoidheight", wpt.geoidheight, writer.precisions["default"])'
        if "name" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement(wpt_, "name", wpt.name)'
        if "cmt" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement(wpt_, "cmt", wpt.cmt)'
        if "desc" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement(wpt_, "desc", wpt.desc)'
        if "src" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement(wpt_, "src", wpt.src)'
        if "link" in fields:
            code += "\n\t\tfor l in wpt.link:"
            code += "\n\t\t\twpt_ = writer.add_link(wpt_, l)"
        if "sym" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement(wpt_, "sym", wpt.sym)'
        if "type" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement(wpt_, "type", wpt.type)'
        if "fix" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement(wpt_, "fix", writer.get_value(wpt.fix))'
        if "sat" in fields:
            code += (
                '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "sat", wpt.sat, 0)'
            )
        if "hdop" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "hdop", wpt.hdop, writer.precisions["default"])'
        if "vdop" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "vdop", wpt.vdop, writer.precisions["default"])'
        if "pdop" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "pdop", wpt.pdop, writer.precisions["default"])'
        if "ageofdgpsdata" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "ageofdgpsdata", wpt.ageofdgpsdata, writer.precisions["default"])'
        if "dgpsid" in fields:
            code += '\n\t\twpt_, _ = writer.add_subelement_number(wpt_, "dgpsid", writer.get_value(wpt.dgpsid), 0)'
        if "extensions" in fields:
            code += '\n\t\twpt_ = writer.add_extensions(wpt_, wpt.extensions, writer.extensions_fields.get("trkpt"))'
        code += "\n\treturn element"
        return FunctionType(
            compile(code, "<_add_trkpt>", "exec").co_consts[0],
            globals(),
            "_add_trkpt",
        )
