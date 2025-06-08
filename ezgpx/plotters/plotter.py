import pandas as pd

from ..gpx import GPX


class Plotter:
    """
    GPX plotter (parent class).
    """

    def __init__(self, gpx: GPX) -> None:
        self._gpx: GPX = gpx

        # self._background: str = None
        # self._color: str = "#FFA800"
        # self._start_color: str = "#00FF00"
        # self._stop_color: str = "#FF0000"
        # self._way_points_color: str = "#0000FF"
        # self._title: str = None
        # self._file_path: str = None

        self._dataframe: pd.DataFrame = None

    def plot(self): ...
