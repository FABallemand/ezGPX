import os
import logging
from typing import Optional, Tuple
from math import isclose
import numpy as np
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# from ..gpx import GPX
from .plotter import Plotter

class MatplotlibAnimPlotter(Plotter):

    # def __init__(self, gpx: GPX) -> None:
    #     super().__init__(gpx)

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
            interval: float = 20,
            fps: int = 24,
            bitrate: int = 1800,
            repeat: bool = True,
            title: Optional[str] = None,
            title_fontsize: int = 20,
            watermark: bool = False,
            file_path: str = None):
        """
        Crashes may be due to parametres exceeding system capabilities.
        Try reducing fps and/or bitrate.
        """
        # Create dataframe containing data from the GPX file
        self._dataframe = self._gpx.to_pandas()

        # Retrieve useful data
        lat = self._dataframe["lat"].values
        lon = self._dataframe["lon"].values

        # Create figure
        fig = plt.figure(figsize=figsize)

        # Compute track boundaries
        min_lat, min_lon, max_lat, max_lon = self._gpx.bounds()

        # Add default offset
        delta_max = max(max_lat - min_lat, max_lon - min_lon)
        offset = delta_max * offset_percentage
        min_lat, min_lon = max(0, min_lat - offset), max(0, min_lon - offset)
        max_lat, max_lon = min(
            max_lat + offset, 90),  min(max_lon + offset, 180)

        # Some sort of magic to achieve the correct map aspect ratio
        # CREATE FUNCTION (also used in anmation??)
        lat_offset = 1e-5
        lon_offset = 1e-5
        delta_lat = max_lat - min_lat
        delta_lon = max_lon - min_lon
        r = delta_lon / delta_lat  # Current map aspect ratio
        # Target map aspect ratio, Adapt in function of the shape of the subplot...
        r_ref = figsize[0] / figsize[1]

        tolerance = 1e-3
        # while (not isclose(r, r_ref, abs_tol=tolerance) or
        #        not isclose(delta_lon % pos.width, 0.0, abs_tol=tolerance) or
        #        not isclose(delta_lat % pos.height, 0.0, abs_tol=tolerance)):
        while not isclose(r, r_ref, abs_tol=tolerance):
            if r > r_ref:
                min_lat = max(0, min_lat - lat_offset)
                max_lat = min(max_lat + lat_offset, 90)
                delta_lat = max_lat - min_lat
            if r < r_ref:
                min_lon = max(0, min_lon - lon_offset)
                max_lon = min(max_lon + lon_offset, 180)
                delta_lon = max_lon - min_lon
            r = delta_lon / delta_lat

        # Create map
        map = Basemap(projection="cyl", llcrnrlon=min_lon, llcrnrlat=min_lat,
                      urcrnrlon=max_lon, urcrnrlat=max_lat)

        # Add background
        if background is None:
            pass
        elif background == "bluemarble":
            map.bluemarble()
        elif background == "shadedrelief":
            map.shadedrelief()
        elif background == "etopo":
            map.etopo()
        elif background == "wms":
            wms_server = "http://www.ga.gov.au/gis/services/topography/Australian_Topography/MapServer/WMSServer"
            wms_server = "http://wms.geosignal.fr/metropole?"
            map.wmsimage(wms_server,
                         layers=["Communes", "Nationales", "Regions"],
                         verbose=True)
        else:
            map.arcgisimage(service=background, dpi=dpi, verbose=True)

        # Create empty line
        # Add marker, marker style...
        line, = fig.gca().plot([], [], color=color, linewidth=size)

        # Animation function
        def animate(i):
            # Clear line at the beginning of the animation
            if i == 0:
                line.set_xdata([])
                line.set_ydata([])

            try:
                line.set_xdata(np.concatenate(
                    (line.get_xdata(), np.array([lon[i]]))))
                line.set_ydata(np.concatenate(
                    (line.get_ydata(), np.array([lat[i]]))))
            except:
                print("No more data point, you need to stop!!")

            return line,

        # Create animation
        ani = animation.FuncAnimation(fig=fig, func=animate, frames=len(lat),
                                      interval=interval,  # Delay between frames in ms
                                      repeat=repeat if file_path is None else False)  # ?

        # Colorbar
        # if colorbar:
        #     fig.colorbar(im)

        # Add title
        if title is not None:
            if watermark:
                fig.suptitle(
                    title + "\n[made with ezGPX]", fontsize=title_fontsize)
            else:
                fig.suptitle(title, fontsize=title_fontsize)

        # Set figure layout
        fig.tight_layout()

        # Save or display plot
        if file_path is not None:
            # Check if provided path exists
            directory_path = os.path.dirname(os.path.realpath(file_path))
            if not os.path.exists(directory_path):
                logging.error("Provided path does not exist")
                return
            # ani.save(file_path, fps=fps, dpi=dpi)
            writer = None
            if file_path.endswith(".mp4"):
                writer = animation.FFMpegWriter(fps=fps,
                                                metadata=dict(artist="ezGPX"),
                                                bitrate=bitrate)
            elif file_path.endswith(".gif"):
                writer = animation.PillowWriter(fps=fps,
                                                metadata=dict(artist="ezGPX"),
                                                bitrate=bitrate)
            ani.save(file_path, writer=writer)
        else:
            # ani.show()
            pass

        return fig
