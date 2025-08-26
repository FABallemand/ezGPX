import os
import warnings
from typing import Optional

import plotly.graph_objects as go

from .plotter import Plotter


class PlotlyPlotter(Plotter):
    """
    GPX plotter based on Plotly.
    """

    def plot(
        self,
        tiles: str = "open-street-map",  # "open-street-map"
        mode: str = "lines",  # "lines", "markers+lines"
        color: str = "#FFA800",
        start_point_color: Optional[str] = None,
        stop_point_color: Optional[str] = None,
        way_points_color: Optional[str] = None,
        title: Optional[str] = None,
        zoom: float = 12.0,
        file_path: Optional[str] = None,
    ):
        """
        Plot (animation) GPX using Plotly.

        Args:
            tiles (str, optional): Map tiles to use. Defaults to
                "open-street-map".
            start_point_color (Optional[str], optional): Color of the
                first point. Defaults to None.
            stop_point_color (Optional[str], optional): Color of the
                last point. Defaults to None.
            way_points_color (Optional[str], optional): Color of the
                way points. Defaults to None.
            title (Optional[str], optional): Title of the plot.
                Defaults to None.
            zoom (float, optional): Zoom. Defaults to 12.0.
            file_path (Optional[str], optional): Path to save the plot. Defaults to None.

        Returns:
            _type_: _description_
        """
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
        if start_point_color:
            fig.add_trace(
                go.Scattermap(
                    mode="markers",
                    lon=[self._dataframe["lon"].iloc[0]],
                    lat=[self._dataframe["lat"].iloc[0]],
                    marker={"size": 5, "color": start_point_color},
                )
            )
        if stop_point_color:
            fig.add_trace(
                go.Scattermap(
                    mode="markers",
                    lon=[self._dataframe["lon"].iloc[-1]],
                    lat=[self._dataframe["lat"].iloc[-1]],
                    marker={"size": 5, "color": stop_point_color},
                )
            )

        # Scatter way points with different color
        if way_points_color:
            for way_point in self._gpx.gpx.wpt:
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

        # Save plot
        if file_path is not None:
            # Check if provided path exists
            directory_path = os.path.dirname(os.path.realpath(file_path))
            if not os.path.exists(directory_path):
                warnings.warn("Provided path does not exist")
                return
            if file_path.endswith(".html"):
                fig.write_html(file_path)
            elif file_path.endswith(".json"):
                fig.write_json(file_path)
            else:
                fig.write_image(file_path)

        return fig
