import logging
import datetime

from ..gpx_elements import Extensions, Link
from ..utils import web_mercator_projection

class WayPoint():
    """
    Way point (wpt) element in GPX file.
    """

    def __init__(
            self,
            lat: float = None,
            lon: float = None,
            ele: float = None,
            time: datetime = None,
            mag_var: float = None,
            geoid_height: float = None,
            name: str = None,
            cmt: str = None,
            desc: str = None,
            src: str = None,
            link: Link = None,
            sym: str = None,
            type: str = None,
            fix: str = None, # none, 2d, 3d, dgps, pps
            sat: int = None, # non negative
            hdop: float = None,
            vdop: float = None,
            pdop: float = None,
            age_of_gps_data: float = None,
            dgpsid: int = None, # 0<=value<=1023
            extensions: Extensions = None) -> None:
        self.lat: float = lat
        self.lon: float = lon
        self.ele: float = ele
        self.time: datetime = time
        self.mag_var: float = mag_var
        self.geoid_height: float = geoid_height
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

        self._x: int = None
        self._y: int = None

    def project(self):
        self._x, self._y = web_mercator_projection(self.latitude, self.longitude)