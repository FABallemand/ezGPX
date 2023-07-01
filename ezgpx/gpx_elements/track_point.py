import datetime

from ..utils import web_mercator_projection

class TrackPoint():
    """
    Track point (trkpt) element in GPX file.
    """

    def __init__(
            self,
            latitude: float = None,
            longitude: float = None,
            elevation: float = None,
            time: datetime = None) -> None:
        """
        Initialize TrackPoint instance.

        Args:
            latitude (float, optional): Latitude. Defaults to None.
            longitude (float, optional): Longitude. Defaults to None.
            elevation (float, optional): Elevation. Defaults to None.
            time (datetime, optional): Time. Defaults to None.
        """
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.elevation: float = elevation
        self.time: datetime = time

        self._x: int = None
        self._y: int = None

    def project(self):
        self._x, self._y = web_mercator_projection(self.latitude, self.longitude)

    