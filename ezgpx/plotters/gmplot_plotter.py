import webbrowser
from typing import Optional, Tuple

import gmplot

from .plotter import Plotter


class GmplotPlotter(Plotter):
    """
    GPX plotter based on gmplot.
    """

    def plot(
        self,
        color: str = "#FFA800",
        start_stop_colors: Optional[Tuple[str, str]] = None,
        way_points_color: Optional[str] = None,
        scatter: bool = False,
        plot: bool = True,
        zoom: float = 10.0,
        title: Optional[str] = None,
        file_path: Optional[str] = None,
        browser: bool = True,
    ):
        """
        Plot GPX using gmplot.

        Args:
            color (str, optional): Track color. Defaults to "#FFA800".
            start_stop_colors (Optional[Tuple[str, str]], optional):
                Start and stop points colors. Defaults to None.
            way_points_color (Optional[str], optional): Way points
                color. Defaults to None.
            scatter (bool, optional): Scatter track points. Defaults
                to False.
            plot (bool, optional): Plot track points. Defaults to True.
            zoom (float, optional): Zoom. Defaults to 10.0.
            title (Optional[str], optional): Title of the plot.
                Defaults to None.
            file_path (Optional[str], optional): Path to save plot.
                Defaults to None.
            browser (bool, optional): Open the plot in the default
                web browser. Defaults to True.
        """
        # Create plotter
        c_lat, c_lon = self._gpx.center()
        map_ = gmplot.GoogleMapPlotter(c_lat, c_lon, zoom)

        # Create dataframe containing data from the GPX file
        gpx_df = self._gpx.to_pandas()

        # Scatter track points
        if scatter:
            map_.scatter(gpx_df["lat"], gpx_df["lon"], color, size=5, marker=False)
        if plot:
            map_.plot(gpx_df["lat"], gpx_df["lon"], color, edge_width=2.5)

        # Scatter start and stop points with different color
        if start_stop_colors:
            map_.scatter(
                [self._gpx.gpx.trk[0].trkseg[0].trkpt[0].lat],
                [self._gpx.gpx.trk[0].trkseg[0].trkpt[0].lon],
                start_stop_colors[0],
                size=5,
                marker=True,
            )
            map_.scatter(
                [self._gpx.gpx.trk[-1].trkseg[-1].trkpt[-1].lat],
                [self._gpx.gpx.trk[-1].trkseg[-1].trkpt[-1].lon],
                start_stop_colors[1],
                size=5,
                marker=True,
            )

        # Scatter way points with different color
        if way_points_color:
            for way_point in self._gpx.gpx.wpt:
                map_.scatter(
                    [way_point.lat],
                    [way_point.lon],
                    way_points_color,
                    size=5,
                    marker=True,
                )

        # Add title
        if title is not None:
            map_.text(c_lat, c_lon, self._gpx.name(), color="#FFFFFF")

        # Save map
        if file_path is None:
            file_path = self._gpx.file_path[:-4] + ".html"
        map_.draw(file_path)

        # Open map in web browser
        if browser:
            webbrowser.open(file_path)
