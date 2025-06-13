import logging
import os
from typing import Optional, Tuple

import numpy as np
import pandas as pd
import plotly.express as px

from .plotter import Plotter


class PlotlyAnimPlotter(Plotter):
    def plot(
        self,
        tiles: str = "open-street-map",  # "open-street-map"
        color: str = "#FFA800",
        title: Optional[str] = None,
        zoom: float = 12.0,
        file_path: Optional[str] = None,
    ):
        self._dataframe = self._gpx.to_pandas()
        center_lat, center_lon = self._gpx.center()
        start = 0
        n_points = len(self._dataframe)

        # Create dataframe for animation
        df = pd.DataFrame()
        for i in np.arange(start, n_points):
            dfa = self._dataframe.head(i).copy()
            dfa["frame"] = i
            df = pd.concat([df, dfa])

        # plotly figure
        fig = px.line_map(df, lat="lat", lon="lon", animation_frame="frame")

        # attribute adjusments
        fig.layout.updatemenus[0].buttons[0]["args"][1]["frame"]["redraw"] = True
        fig.layout.updatemenus[0].buttons[0]["args"][1]["frame"]["duration"] = 0.25
        fig.layout.updatemenus[0].buttons[0]["args"][1]["transition"]["duration"] = 0.25

        # Update layout for nice display
        fig.update_layout(
            margin={"l": 0, "t": 0, "b": 0, "r": 0},
            map={
                "center": {"lon": center_lon, "lat": center_lat},
                "style": tiles,
                "zoom": zoom,
            },
            title={"text": title},
        )

        # Save plot
        if file_path is not None:
            # Check if provided path exists
            directory_path = os.path.dirname(os.path.realpath(file_path))
            if not os.path.exists(directory_path):
                logging.error("Provided path does not exist")
                return
            if file_path.endswith(".html"):
                fig.write_html(file_path)
            else:
                fig.write_image(file_path)

        return fig
