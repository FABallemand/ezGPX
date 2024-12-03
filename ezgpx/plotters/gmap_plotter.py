from typing import Optional, Tuple
import webbrowser
import gmplot

# from ..gpx import GPX
from .plotter import Plotter

class GmapPlotter(Plotter):
    """
    GPX object plotter (using gmap).
    """

    # def __init__(self, gpx: GPX) -> None:
    #     super().__init__(gpx)

    def plot(
            self,
            color: str = "#110000",
            start_stop_colors: Optional[Tuple[str, str]] = None,
            way_points_color: Optional[str] = None,
            scatter: bool = False,
            plot: bool = True,
            zoom: float = 10.0,
            title: Optional[str] = None,
            file_path: str = None,
            browser: bool = True):
        """
        Plot GPX using gmplot.

        Parameters
        ----------
        color : str, optional
            Track color, by default "#110000"
        start_stop_colors : Optional[Tuple[str, str]], optional
            Start and stop points colors, by default None
        way_points_color : Optional[str], optional
            Way points color, by default None
        scatter : bool, optional
            Scatter track points, by default False
        plot : bool, optional
            Plot track points, by default True
        zoom : float, optional
            Zoom, by default 10.0
        title : Optional[str], optional
            Title, by default None
        file_path : str, optional
            Path to save plot, by default None
        browser : bool, optional
            Open the plot in the default web browser, by default True
        """
        # Create plotter
        c_lat, c_lon = self.gpx.center()
        map = gmplot.GoogleMapPlotter(c_lat, c_lon, zoom)

        # Create dataframe containing data from the GPX file
        gpx_df = self.gpx.to_dataframe()

        # Scatter track points
        if scatter:
            map.scatter(gpx_df["lat"], gpx_df["lon"],
                        color, size=5, marker=False)
        if plot:
            map.plot(gpx_df["lat"], gpx_df["lon"],
                     color, edge_width=2.5)

        # Scatter start and stop points with different color
        if start_stop_colors:
            map.scatter([self.gpx.trk[0].trkseg[0].trkpt[0].lat],
                        [self.gpx.trk[0].trkseg[0].trkpt[0].lon],
                        start_stop_colors[0], size=5, marker=True)
            map.scatter([self.gpx.trk[-1].trkseg[-1].trkpt[-1].lat],
                        [self.gpx.trk[-1].trkseg[-1].trkpt[-1].lon],
                        start_stop_colors[1], size=5, marker=True)

        # Scatter way points with different color
        if way_points_color:
            for way_point in self.gpx.wpt:
                map.scatter([way_point.lat], [way_point.lon],
                            way_points_color, size=5, marker=True)

        # Add title
        if title is not None:
            map.text(c_lat, c_lon, self.gpx.name(), color="#FFFFFF")

        # Save map
        map.draw(file_path)

        # Open map in web browser
        if browser:
            webbrowser.open(file_path)