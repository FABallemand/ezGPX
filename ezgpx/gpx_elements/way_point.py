import logging
import datetime

from .extensions import Extensions
from .link import Link
from ..utils import web_mercator_projection, lambert_conformal_conic_projection

class WayPoint():
    """
    wptType element in GPX file.
    """

    def __init__(
            self,
            tag: str = "wpt",
            lat: float = None,
            lon: float = None,
            ele: float = None,
            time: datetime = None,
            mag_var: float = None, # 0 <= value < 360
            geo_id_height: float = None,
            name: str = None,
            cmt: str = None,
            desc: str = None,
            src: str = None,
            link: Link = None,
            sym: str = None,
            type: str = None,
            fix: str = None, # none, 2d, 3d, dgps, pps
            sat: int = None, # non negative integer
            hdop: float = None,
            vdop: float = None,
            pdop: float = None,
            age_of_gps_data: float = None,
            dgpsid: int = None, # 0 <= value <= 1023
            extensions: Extensions = None) -> None:
        """
        Initialize WayPoint instance.

        Args:
            tag (str, optional): XML tag. Defaults to "wpt".
            lat (float, optional): Latitude. Defaults to None.
            lon (float, optional): Longitude. Defaults to None.
            ele (float, optional): Elevation. Defaults to None.
            time (datetime, optional): Time. Defaults to None.
            mag_var (float, optional): _description_. Defaults to None.
            geo_id_height (float, optional): _description_. Defaults to None.
            name (str, optional): Name. Defaults to None.
            cmt (str, optional): Comment. Defaults to None.
            desc (str, optional): Description. Defaults to None.
            src (str, optional): Source. Defaults to None.
            link (Link, optional): link. Defaults to None.
            sym (str, optional): _description_. Defaults to None.
            type (str, optional): Type. Defaults to None.
            fix (str, optional): _description_. Defaults to None.
            ppssat (int, optional): _description_. Defaults to None.
            vdop (float, optional): _description_. Defaults to None.
            pdop (float, optional): _description_. Defaults to None.
            age_of_gps_data (float, optional): Age of GPS data. Defaults to None.
            dgpsid (int, optional): _description_. Defaults to None.
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

        # Statistics (for map plotting: https://support.strava.com/hc/en-us/articles/360049869011-Personalized-Stat-Maps)
        self.speed: float = None
        self.pace: float = None
        self.ascent_rate: float = None
        self.ascent_speed: float = None

        # Projection
        self._x: int = None
        self._y: int = None

    def project(self, projection: str):
        """
        Project point.

        Args:
            projection (str): Projection.
        """
        if projection in ["web_mercator_projection", "web_mercator", "wm"]:
            self._x, self._y = web_mercator_projection(self.lat, self.lon)
        elif projection in ["lambert_conformal_conic_projection", "lambert_conformal_conic", "lcc"]:
            self._x, self._y = lambert_conformal_conic_projection(self.lat, self.lon, 90.0, 135.0, 45.0, 45.0)
        else:
            logging.error(f"Invalid projection: {projection}")
