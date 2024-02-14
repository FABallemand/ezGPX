import datetime

class Point():
    """
    ptType element in GPX file.
    """

    def __init__(
            self,
            tag: str = "pt",
            lat: float = None,
            lon: float = None,
            ele: float = None,
            time: datetime = None) -> None:
        """
        Initialize Point instance.

        Parameters
        ----------
        tag : str, optional
            XML tag, by default "pt"
        lat : float, optional
            Latitude, by default None
        lon : float, optional
            Longitude, by default None
        ele : float, optional
            Elevation, by default None
        time : datetime, optional
            Time, by default None
        """
        self.tag: str = tag
        self.lat: float = lat
        self.lon: float = lon
        self.ele: float = ele
        self.time: datetime = time

    