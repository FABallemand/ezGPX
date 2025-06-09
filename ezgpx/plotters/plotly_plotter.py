import logging
import os
from typing import Optional, Tuple

import plotly.graph_objects as go

from .plotter import Plotter


class PlotlyPlotter(Plotter):
    def plot(
        self,
        tiles: str = "open-street-map",  # "open-street-map"
        mode: str = "lines",  # "lines", "markers+lines"
        color: str = "#FFA800",
        start_stop_colors: Optional[Tuple[str, str]] = None,
        way_points_color: Optional[str] = None,
        title: Optional[str] = None,
        zoom: float = 12.0,
        file_path: Optional[str] = None,
    ):
        self._dataframe = self._gpx.to_pandas()
        center_lat, center_lon = self._gpx.center()

        # Create map and scatter
        fig = go.Figure(
            go.Scattermap(
                mode=mode,
                lon=self._dataframe["lon"],
                lat=self._dataframe["lat"],
                marker={"size": 5, "color": color},
            )
        )

        # Scatter start and stop points with different color
        if start_stop_colors:
            fig.add_trace(
                go.Scattermap(
                    mode="markers",
                    lon=[self._dataframe["lon"].iloc[0]],
                    lat=[self._dataframe["lat"].iloc[0]],
                    marker={"size": 5, "color": start_stop_colors[0]},
                )
            )
            fig.add_trace(
                go.Scattermap(
                    mode="markers",
                    lon=[self._dataframe["lon"].iloc[-1]],
                    lat=[self._dataframe["lat"].iloc[-1]],
                    marker={"size": 5, "color": start_stop_colors[1]},
                )
            )

        # Scatter way points with different color
        if way_points_color:
            for way_point in self._gpx.wpt:
                fig.add_trace(
                    go.Scattermap(
                        mode="markers",
                        lon=way_point.lon,
                        lat=way_point.lat,
                        marker={"size": 5, "color": way_points_color},
                    )
                )

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

        # Save or display plot
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
        else:
            fig.show()

        return fig
