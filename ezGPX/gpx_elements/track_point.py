from typing import *

class TrackPoint():

    def __init__(self, lat: float = None, lon: float = None, ele: float = None, time: str = None):
        self.lat = lat
        self.lon = lon
        self.ele = ele
        self.time = time

    