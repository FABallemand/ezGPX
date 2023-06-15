import datetime

class TrackPoint():
    """
    Track point (trkpt) elevationment in GPX file.
    """

    def __init__(self, latitude: float = None, longitude: float = None, elevation: float = None, time: datetime = None):
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.elevation: float = elevation
        self.time: datetime = time

    