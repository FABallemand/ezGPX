import logging
import os
from math import isclose
from typing import Optional, Tuple

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from .plotter import Plotter


class MatplotlibPlotter(Plotter):
    def plot(
        self,
        figsize: Tuple[int, int] = (16, 9),
        size: float = 10,
        color: str = "#101010",
        cmap: Optional[matplotlib.colors.Colormap] = None,
        colorbar: bool = False,
        start_point_color: Optional[str] = None,
        stop_point_color: Optional[str] = None,
        way_points_color: Optional[str] = None,
        background: Optional[str] = None,
        offset_percentage: float = 0.04,
        dpi: int = 96,
        title: Optional[str] = None,
        title_fontsize: int = 20,
        watermark: bool = False,
        file_path: str = None,
    ):

        dynamic_colors = [
            "ele",
            "speed",
            "pace",
            "vertical_drop",
            "ascent_rate",
            "ascent_speed",
        ]

        # Create dataframe containing data from the GPX file
        values = ["lat", "lon"]
        if color in dynamic_colors:
            values.append(color)
        self._dataframe = self._gpx.to_pandas(values)

        # Create figure
        fig = plt.figure(figsize=figsize)

        # Compute track boundaries
        min_lat, min_lon, max_lat, max_lon = self._gpx.bounds()

        # Compute default offset
        delta_lat = abs(max_lat - min_lat)
        delta_lon = abs(max_lon - min_lon)
        delta_max = max(delta_lat, delta_lon)
        offset = delta_max * offset_percentage

        # Add default offset
        min_lat = max(-90, min_lat - offset)
        max_lat = min(max_lat + offset, 90)
        min_lon = max(-180, min_lon - offset)
        max_lon = min(max_lon + offset, 180)

        # Some sort of magic to achieve the correct map aspect ratio
        # CREATE FUNCTION (also used in animation??)
        lat_offset = 1e-5
        lon_offset = 1e-5
        delta_lat = abs(max_lat - min_lat)
        delta_lon = abs(max_lon - min_lon)
        r = delta_lon / delta_lat  # Current map aspect ratio
        # Target map aspect ratio, Adapt in function of the shape of the subplot...
        r_ref = figsize[0] / figsize[1]

        tolerance = 1e-3
        # while (not isclose(r, r_ref, abs_tol=tolerance) or
        #        not isclose(delta_lon % pos.width, 0.0, abs_tol=tolerance) or
        #        not isclose(delta_lat % pos.height, 0.0, abs_tol=tolerance)):
        while not isclose(r, r_ref, abs_tol=tolerance):
            if r > r_ref:
                min_lat = max(-90, min_lat - lat_offset)
                max_lat = min(max_lat + lat_offset, 90)
                delta_lat = max_lat - min_lat
            if r < r_ref:
                min_lon = max(-180, min_lon - lon_offset)
                max_lon = min(max_lon + lon_offset, 180)
                delta_lon = max_lon - min_lon
            r = delta_lon / delta_lat

        # Create map
        map_ = Basemap(
            projection="cyl",
            llcrnrlon=min_lon,
            llcrnrlat=min_lat,
            urcrnrlon=max_lon,
            urcrnrlat=max_lat,
        )

        # Add background
        if background is None:
            pass
        elif background == "bluemarble":
            map_.bluemarble()
        elif background == "shadedrelief":
            map_.shadedrelief()
        elif background == "etopo":
            map_.etopo()
        elif background == "wms":
            wms_server = "http://www.ga.gov.au/gis/services/topography/Australian_Topography/MapServer/WMSServer"
            wms_server = "http://wms.geosignal.fr/metropole?"
            map_.wmsimage(
                wms_server, layers=["Communes", "Nationales", "Regions"], verbose=True
            )
        else:
            map_.arcgisimage(service=background, dpi=dpi, verbose=True)

        # Scatter track points
        if color in dynamic_colors:
            im = map_.scatter(
                self._dataframe["lon"],
                self._dataframe["lat"],
                s=size,
                c=self._dataframe[color],
                cmap=cmap,
            )
        else:
            im = map_.scatter(
                self._dataframe["lon"], self._dataframe["lat"], s=size, color=color
            )

        # Scatter start point with different color
        if start_point_color:
            map_.scatter(
                self._dataframe["lon"][0],
                self._dataframe["lat"][0],
                marker="^",
                color=start_point_color,
            )

        # Scatter stop point with different color
        if stop_point_color:
            map_.scatter(
                self._dataframe["lon"].iloc[-1],
                self._dataframe["lat"].iloc[-1],
                marker="h",
                color=stop_point_color,
            )

        # Scatter way points with different color
        if way_points_color:
            for way_point in self._gpx.wpt:
                x, y = map_(way_point.lon, way_point.lat)  # Project way point
                map_.scatter(
                    x, y, marker="D", color=way_points_color
                )  # Scatter way point

        # Colorbar
        if colorbar:
            fig.colorbar(im)

        # Add title
        if title is not None:
            if watermark:
                fig.suptitle(title + "\n[made with ezGPX]", fontsize=title_fontsize)
            else:
                fig.suptitle(title, fontsize=title_fontsize)

        # Set figure layout
        fig.tight_layout()

        # Save plot
        if file_path is not None:
            # Check if provided path exists
            directory_path = os.path.dirname(os.path.realpath(file_path))
            if not os.path.exists(directory_path):
                logging.error("Provided path does not exist")
                return
            fig.savefig(file_path)

        return fig
