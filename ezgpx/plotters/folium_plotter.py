from typing import Optional, Tuple
import webbrowser
import folium
from folium.features import DivIcon
from folium.plugins import MiniMap

# from ..gpx import GPX
from .plotter import Plotter

class FoliumPlotter(Plotter):

    # def __init__(self, gpx: GPX) -> None:
    #     super().__init__(gpx)

    def plot(
            self,
            tiles: str = "OpenStreetMap",  # "OpenStreetMap", "Stamen Terrain", "Stamen Toner"
            color: str = "#110000",
            start_stop_colors: Optional[Tuple[str, str]] = None,
            way_points_color: Optional[str] = None,
            minimap: bool = False,
            coord_popup: bool = False,
            title: Optional[str] = None,
            zoom: float = 12.0,
            file_path: Optional[str] = None,
            browser: bool = True):
        """
        Plot GPX using folium.

        Parameters
        ----------
        tiles : str, optional
            Map tiles. Supported tiles: "OpenStreetMap", "Stamen Terrain",
            "Stamen Toner", by default "OpenStreetMap"
        start_stop_colors : Optional[Tuple[str, str]], optional
            Start and stop points colors, by default None
        way_points_color : Optional[str], optional
            Way points color, by default None
        minimap : bool, optional
            Add minimap, by default False
        coord_popup : bool, optional
            Add coordinates pop-up when clicking on the map, by default False
        title : Optional[str], optional
            Title, by default None
        zoom : float, optional
            Zoom, by default 12.0
        file_path : str, optional
            Path to save plot, by default None
        browser : bool, optional
            Open the plot in the default web browser, by default True
        """
        # Create map
        center_lat, center_lon = self.gpx.center()
        m = folium.Map(location=[center_lat, center_lon],
                       zoom_start=zoom,
                       tiles=tiles)

        # Plot track points
        gpx_df = self.gpx.to_pandas()
        gpx_df["coordinates"] = list(
            zip(gpx_df.lat, gpx_df.lon))
        folium.PolyLine(gpx_df["coordinates"],
                        tooltip=self.gpx.name(), color=color).add_to(m)

        # Scatter start and stop points with different color
        if start_stop_colors:
            folium.Marker([self.gpx.trk[0].trkseg[0].trkpt[0].lat, self.gpx.trk[0].trkseg[0].trkpt[0].lon],
                          popup="<b>Start</b>", tooltip="Start", icon=folium.Icon(color=start_stop_colors[0])).add_to(m)
            folium.Marker([self.gpx.trk[-1].trkseg[-1].trkpt[-1].lat, self.gpx.trk[-1].trkseg[-1].trkpt[-1].lon],
                          popup="<b>Stop</b>", tooltip="Stop", icon=folium.Icon(color=start_stop_colors[1])).add_to(m)

        # Scatter way points with different color
        if way_points_color:
            for way_point in self.gpx.wpt:
                folium.Marker([way_point.lat, way_point.lon], popup="<i>Way point</i>",
                              tooltip="Way point", icon=folium.Icon(icon="info-sign", color=way_points_color)).add_to(m)

        # Add minimap
        if minimap:
            minimap = MiniMap(toggle_display=True)
            minimap.add_to(m)

        # Add latitude-longitude pop-up
        if coord_popup:
            m.add_child(folium.LatLngPopup())

        # Title
        if title is not None:
            folium.map.Marker(
                [center_lat, center_lon],
                icon=DivIcon(
                    icon_size=(250, 36),
                    icon_anchor=(0, 0),
                    html=f'<div style="font-size: 20pt">{title}</div>',
                )
            ).add_to(m)

        # Save map
        if file_path is None:
            file_path = file_path[:-4] + ".html"
        m.save(file_path)

        # Open map in web browser
        if browser:
            webbrowser.open(file_path)
