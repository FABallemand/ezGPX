import logging
import datetime

from .extensions import Extensions
from .link import Link

class WayPoint():
    """
    wptType element in GPX file.
    """
    fields = ["lat", "lon", "ele", "time", "mag_var", "geo_id_height", "name",
              "cmt", "desc", "src", "link", "sym", "type", "fix", "sat",
              "hdop", "vdop", "pdop", "age_of_gps_data", "dgpsid", "extensions"]
    mandatory_fields = ["lat", "lon"]

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

        Parameters
        ----------
        tag : str, optional
            XML tag, by default "wpt"
        lat : float, optional
            Latitude (degrees), by default None
        lon : float, optional
            Longitude (degrees), by default None
        ele : float, optional
            Elevation (meters), by default None
        time : datetime, optional
            Time, by default None
        mag_var : float, optional
            Magnetic variation (degrees) at the point, by default None
        geo_id_height : float, optional
            Height (meters) of geoid (mean sea level) above WGS84 earth
            ellipsoid. As defined in NMEA GGA message., by default None
        name : str, optional
            Name, by default None
        cmt : str, optional
            Comment, by default None
        desc : str, optional
            Description, by default None
        src : str, optional
            Source, by default None
        link : Link, optional
            Link, by default None
        sym : str, optional
            Text of GPS symbol name. For interchange with other programs,
            use the exact spelling of the symbol as displayed on the GPS.
            If the GPS abbreviates words, spell them out, by default None
        type : str, optional
            Type, by default None
        fix : str, optional
            Type of GPX fix, by default None
        sat : int, optional
            Number of satellites used to calculate the GPX fix, by default None
        hdop : float, optional
            Horizontal dilution of precision, by default None
        vdop : float, optional
            Vertical dilution of precision, by default None
        pdop : float, optional
            Position dilution of precision, by default None
        age_of_gps_data : float, optional
            Number of seconds since last DGPS update, by default None
        dgpsid : int, optional
            ID of DGPS station used in differential correction, by default None
        extensions: Extensions, optional
            Extensions, by default None
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
        self.distance_from_start: float = None
