"""
This module contains the WayPoint class.
"""

import datetime

from .extensions import Extensions
from .gpx_element import GpxElement
from .link import Link


class WayPoint(GpxElement):
    """
    wptType element in GPX file.
    """

    fields = [
        "lat",
        "lon",
        "ele",
        "time",
        "mag_var",
        "geo_id_height",
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
        "age_of_gps_data",
        "dgpsid",
        "extensions",
    ]
    mandatory_fields = ["lat", "lon"]

    def __init__(
        self,
        tag: str = "wpt",
        lat: float = None,
        lon: float = None,
        ele: float = None,
        time: datetime = None,
        mag_var: float = None,  # 0 <= value < 360
        geo_id_height: float = None,
        name: str = None,
        cmt: str = None,
        desc: str = None,
        src: str = None,
        link: Link = None,
        sym: str = None,
        type: str = None,  # pylint: disable=redefined-builtin
        fix: str = None,  # none, 2d, 3d, dgps, pps
        sat: int = None,  # non negative integer
        hdop: float = None,
        vdop: float = None,
        pdop: float = None,
        age_of_gps_data: float = None,
        dgpsid: int = None,  # 0 <= value <= 1023
        extensions: Extensions = None,
    ) -> None:
        """
        Initialise WayPoint instance.

        Args:
            tag (str, optional): XML tag. Defaults to "wpt".
            lat (float, optional): Latitude (in degrees). Defaults to None.
            lon (float, optional): Longitude (in degrees). Defaults to None.
            ele (float, optional): Elevation (in meters). Defaults to None.
            time (datetime, optional): Time. Defaults to None.
            mag_var (float, optional): Magnetic variation (in degrees)
                at the point. Defaults to None.
            geo_id_height (float, optional): Height (in meters) of
                geoid (mean sea level) above WGS84 earth ellipsoid.
                As defined in NMEA GGA message. Defaults to None.
            name (str, optional): Name. Defaults to None.
            cmt (str, optional): Comment. Defaults to None.
            desc (str, optional): Description. Defaults to None.
            src (str, optional): Source. Defaults to None.
            link (Link, optional): Link. Defaults to None.
            sym (str, optional): Text of GPS symbol name. For
                interchange with other programs, use the
                exact spelling of the symbol as displayed on the GPS.
                If the GPS abbreviates words, spell them out. Defaults
                to None.
            type (str, optional): Type. Defaults to None.
            fix (str, optional): Type of GPX fix. Defaults to None.
            sat (int, optional): Number of satellites used to calculate
                the GPX fix. Defaults to None.
            hdop (float, optional): Horizontal dilution of precision.
                Defaults to None.
            vdop (float, optional): Vertical dilution of precision.
                Defaults to None.
            pdop (float, optional): Position dilution of precision.
                Defaults to None.
            age_of_gps_data (float, optional): Number of seconds since
                last DGPS update. Defaults to None.
            dgpsid (int, optional): ID of DGPS station used in
                differential correction. Defaults to None.
            extensions (Extensions, optional): Extensions. Defaults to None.
        """
        self.tag: str = tag
        self.lat: float = lat
        self.lon: float = lon
        self.ele: float = ele
        self.time: datetime = time
        self.mag_var: float = mag_var
        self.geo_id_height: float = geo_id_height
        self.name: str = name
        self.cmt: str = cmt
        self.desc: str = desc
        self.src: str = src
        self.link: Link = link
        self.sym: str = sym
        self.type: str = type
        self.fix: str = fix
        self.sat: int = sat
        self.hdop: float = hdop
        self.vdop: float = vdop
        self.pdop: float = pdop
        self.age_of_gps_data: float = age_of_gps_data
        self.dgpsid: int = dgpsid
        self.extensions: Extensions = extensions

        # Statistics for map plotting
        # https://support.strava.com/hc/en-us/articles/360049869011-Personalized-Stat-Maps
        self.speed: float = None
        self.pace: float = None
        self.ascent_rate: float = None
        self.ascent_speed: float = None
        self.distance_from_start: float = None
