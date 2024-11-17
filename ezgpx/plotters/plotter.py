import pandas as pd

from ..gpx import GPX

class Plotter():
    """
    GPX plotter (parent class).
    """

    def __init__(self, gpx: GPX) -> None:
        self.gpx: GPX = gpx
        self._dataframe: pd.DataFrame = None

    def plot(self): ...