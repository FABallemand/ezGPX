import io
import os
from typing import Optional

import numpy as np
import pandas as pd
import PIL
import plotly.express as px

from .plotter import Plotter


class PlotlyAnimPlotter(Plotter):
    """
    GPX animated plotter based on Plotly.
    """

    def plot(
        self,
        tiles: str = "open-street-map",  # "open-street-map"
        color: str = "#FFA800",
        title: Optional[str] = None,
        zoom: float = 12.0,
        file_path: Optional[str] = None,
    ):
        """
        Plot (animation) GPX using Plotly.

        Args:
            tiles (str, optional): Map tiles to use. Defaults to
                "open-street-map".
            title (Optional[str], optional): Title of the plot.
                Defaults to None.
            zoom (float, optional): Zoom. Defaults to 12.0.
            file_path (Optional[str], optional): Path to save the plot. Defaults to None.

        Raises:
            FileNotFoundError: Provided path does not exist.

        Returns:
            plotly.Figure: Animated plot of the GPX.
        """
        self._dataframe = self._gpx.to_pandas(["lat", "lon", "ele"])
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
        fig = px.line_map(
            df, lat="lat", lon="lon", color=color, animation_frame="frame"
        )

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
                raise FileNotFoundError("Provided path does not exist")
            if file_path.endswith(".html"):
                fig.write_html(file_path)
            elif file_path.endswith(".gif"):
                # Generate image for each step in animation
                frames = []
                for s, fr in enumerate(fig.frames):
                    # Set main traces to appropriate traces within plotly frame
                    fig.update(data=fr.data)
                    # Move slider to correct place
                    fig.layout.sliders[0].update(active=s)
                    # Generate image of current state
                    frames.append(
                        PIL.Image.open(io.BytesIO(fig.to_image(format="png")))
                    )
                # Create animated GIF
                frames[0].save(
                    "test.gif",
                    save_all=True,
                    append_images=frames[1:],
                    optimize=True,
                    duration=500,
                    loop=0,
                )

        return fig
