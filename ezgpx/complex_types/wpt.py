"""
This module contains the Wpt class.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from ..simple_types import Degrees, DgpsStation, Fix, Latitude, Longitude
from .extensions import Extensions
from .link import Link


@dataclass
class Wpt:  # pylint: disable=too-many-instance-attributes
    """
    wptType: wpt represents a waypoint, point of interest, or named
    feature on a map.

    Args:
        lat (Latitude): Latitude of the point (in degrees).
        lon (Longitude): Longitude of the point (in degrees).
        ele (float, optional): Elevation of the point (in meters).
            Defaults to None.
        time (datetime, optional): Creation/modification timestamp for
            element. Date and time in are in Univeral Coordinated Time
            (UTC), not local time! Conforms to ISO 8601 specification
            for date/time representation. Fractional seconds are allowed
            for millisecond timing in tracklogs. Defaults to None.
        magvar (Degrees, optional): Magnetic variation at the point
            (in degrees). Defaults to None.
        geoidheight (float, optional): Height (in meters) of
            geoid (mean sea level) above WGS84 earth ellipsoid.
            As defined in NMEA GGA message. Defaults to None.
        name (str, optional): The GPS name of the waypoint. This field
            will be transferred to and from the GPS. GPX does not place
            restrictions on the length of this field or the characters
            contained in it. It is up to the receiving application to
            validate the field before sending it to the GPS.
            Defaults to None.
        cmt (str, optional): GPS waypoint comment. Sent to GPS as
            comment. Defaults to None.
        desc (str, optional): A text description of the element.
            Holds additional information about the element intended
            for the user, not the GPS. Defaults to None.
        src (str, optional): Source of data. Included to give user some
            idea of reliability and accuracy of data. e.g.: "Garmin
            eTrex", "USGS quad Boston North"... Defaults to None.
        link (list[Link], optional): Link to additional information
            about the waypoint. Defaults to None.
        sym (str, optional): Text of GPS symbol name. For
            interchange with other programs, use the
            exact spelling of the symbol as displayed on the GPS.
            If the GPS abbreviates words, spell them out.
            Defaults to None.
        type (str, optional): Type (classification) of the waypoint.
            Defaults to None.
        fix (Fix, optional): Type of GPX fix. Defaults to None.
        sat (int, optional): Number of satellites used to calculate
            the GPX fix. Defaults to None.
        hdop (float, optional): Horizontal dilution of precision.
            Defaults to None.
        vdop (float, optional): Vertical dilution of precision.
            Defaults to None.
        pdop (float, optional): Position dilution of precision.
            Defaults to None.
        ageofgpsdata (float, optional): Number of seconds since
            last DGPS update. Defaults to None.
        dgpsid (DgpsStation, optional): ID of DGPS station used in
            differential correction. Defaults to None.
        extensions (Extensions, optional): You can add extend GPX by
            adding your own elements from another schema here.
            Defaults to None.
        tag (str, optional): XML tag. Defaults to "wpt".
    """

    lat: Latitude
    lon: Longitude
    ele: float = None
    time: datetime = None
    magvar: Degrees = None
    geoidheight: float = None
    name: str = None
    cmt: str = None
    desc: str = None
    src: str = None
    link: list[Link] = None
    sym: str = None
    type: str = None
    fix: Fix = None
    sat: int = None
    hdop: float = None
    vdop: float = None
    pdop: float = None
    ageofgpsdata: float = None
    dgpsid: DgpsStation = None
    extensions: Extensions = None
    tag: str = "wpt"

    # Statistics for map plotting
    # https://support.strava.com/hc/en-us/articles/360049869011-Personalized-Stat-Maps
    # speed: float = None
    # pace: float = None
    # ascent_rate: float = None
    # ascent_speed: float = None
    # distance_from_start: float = None

    _fields: ClassVar[list[str]] = [
        "lat",
        "lon",
        "ele",
        "time",
        "magvar",
        "geoidheight",
        "name",
        "cmt",
        "desc",
        "src",
        "link",
        "sym",
        "type",
        "fix",
        "sat",
        "hdop",
        "vdop",
        "pdop",
        "ageofgpsdata",
        "dgpsid",
        "extensions",
    ]
    _mandatory_fields: ClassVar[list[str]] = ["lat", "lon"]

    def __post_init__(self):
        if not isinstance(self.lat, Latitude):
            self.lat = Latitude(self.lat)
        if not isinstance(self.lon, Longitude):
            self.lon = Longitude(self.lon)
        if self.ele is not None and not isinstance(self.ele, float):
            self.ele = float(self.ele)
        if self.time is not None and not isinstance(self.time, datetime):
            raise TypeError("`time` must be of type datetime")
        if self.magvar is not None and not isinstance(self.magvar, Degrees):
            self.magvar = Degrees(self.magvar)
        if self.geoidheight is not None and not isinstance(self.geoidheight, float):
            self.geoidheight = float(self.geoidheight)
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)
        if self.cmt is not None and not isinstance(self.cmt, str):
            self.cmt = str(self.cmt)
        if self.desc is not None and not isinstance(self.desc, str):
            self.desc = str(self.desc)
        if self.src is not None and not isinstance(self.src, str):
            self.src = str(self.src)
        if self.link is not None and (
            not isinstance(self.link, list)
            or not all(isinstance(ll, Link) for ll in self.link)
        ):
            raise TypeError("`link` must be of type list[Link]")
        if self.sym is not None and not isinstance(self.sym, str):
            self.sym = str(self.sym)
        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)
        if self.fix is not None and not isinstance(self.fix, Fix):
            self.fix = Fix(self.fix)
        if self.sat is not None and not isinstance(self.sat, int):
            self.sat = int(self.sat)
        if self.hdop is not None and not isinstance(self.hdop, float):
            self.hdop = float(self.hdop)
        if self.vdop is not None and not isinstance(self.vdop, float):
            self.vdop = float(self.vdop)
        if self.pdop is not None and not isinstance(self.pdop, float):
            self.pdop = float(self.pdop)
        if self.ageofgpsdata is not None and not isinstance(self.ageofgpsdata, float):
            self.ageofgpsdata = float(self.ageofgpsdata)
        if self.dgpsid is not None and not isinstance(self.dgpsid, DgpsStation):
            self.dgpsid = DgpsStation(self.dgpsid)
        if self.extensions is not None and not isinstance(self.extensions, Extensions):
            raise TypeError("`extensions` must be of type Extensions")
        if not isinstance(self.tag, str):
            self.tag = str(self.tag)
