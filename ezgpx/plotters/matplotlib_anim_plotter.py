import os
import warnings
from math import isclose
from typing import Optional, Tuple

import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

from .plotter import Plotter


class MatplotlibAnimPlotter(Plotter):
    """
    GPX animated plotter based on Matplotlib.
    """

    def plot(
        self,
        figsize: Tuple[int, int] = (16, 9),
        size: float = 5,
        color: str = "#FFA800",
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
        file_path: str = None,
    ):
        """
        Plot (animation) GPX using Matplotlib.

        Crashes may be due to parametres exceeding system capabilities.
        Try reducing fps and/or bitrate.

        Args:
            figsize (Tuple[int, int], optional): Width and height of
                the plot. Defaults to (16, 9).
            size (float, optional): Size of the track. Defaults to 5.
            color (str, optional): Color of the track. Defaults to
                "#FFA800".
            background (Optional[str], optional): Map tiles to use.
                Possible choice are: None, "bluemarble",
                "shadedrelief", "etopo", "World_Imagery", "wms" or any
                server supported by
                `mpl_toolkits.basemap.Basemap.arcgisimage`. Defaults to
                None.
            offset_percentage (float, optional): Offset percentage to
                apply to the track bounding box. Defaults to 0.04.
            dpi (int, optional): Resolution of the animation. Defaults
                to 96.
            interval (float, optional): Interval between frames of the
                animation. Defaults to 20.
            fps (int, optional): FPS of the animation. Defaults to 24.
            bitrate (int, optional): Bit-rate of the animation.
                Defaults to 1800.
            repeat (bool, optional): Repeat the animation when viewed.
                Defaults to True.
            title (Optional[str], optional): Title of the plot.
                Defaults to None.
            title_fontsize (int, optional): Font size of the title of
                the plot. Defaults to 20.
            watermark (bool, optional): Watermark. Defaults to False.
            file_path (str, optional): Path to save the plot. Defaults
                to None.

        Raises:
            FileNotFoundError: Provided path does not exist.

        Returns:
            matplotlib.Figure: Animated plot of the GPX.
        """
        # Create dataframe containing data from the GPX file
        self._dataframe = self._gpx.to_pandas()

        # Retrieve useful data
        lat = self._dataframe["lat"].values
        lon = self._dataframe["lon"].values

        # Create figure
        fig = plt.figure(figsize=figsize)
        ax = fig.gca()

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

        # Update min/max lat/lon to achieve correct aspect ratio
        lat_offset = 1e-5
        lon_offset = 1e-5
        delta_lat = abs(max_lat - min_lat)
        delta_lon = abs(max_lon - min_lon)
        r = delta_lon / delta_lat  # Current map aspect ratio
        r_ref = figsize[0] / figsize[1]  # Target map aspect ratio
        tolerance = 1e-3
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
            ax=ax,
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
        elif background == "World_Imagery":
            map_.arcgisimage(service=background, dpi=dpi)
        elif background == "wms":
            wms_server = "http://www.ga.gov.au/gis/services/topography/Australian_Topography/MapServer/WMSServer"
            wms_server = "http://wms.geosignal.fr/metropole?"
            map_.wmsimage(
                wms_server, layers=["Communes", "Nationales", "Regions"], verbose=True
            )
        else:
            map_.arcgisimage(service=background, dpi=dpi, verbose=True)

        # Create empty line
        (line,) = fig.gca().plot([], [], color=color, linewidth=size)

        # Animation function
        def animate(i):
            # Clear line at the beginning of the animation
            if i == 0:
                line.set_xdata([])
                line.set_ydata([])
            try:
                line.set_xdata(np.concatenate((line.get_xdata(), np.array([lon[i]]))))
                line.set_ydata(np.concatenate((line.get_ydata(), np.array([lat[i]]))))
            except IndexError:
                warnings.warn("No more data point, you need to stop!!")

            return line

        # Create animation
        ani = animation.FuncAnimation(
            fig=fig,
            func=animate,
            frames=len(lat),
            interval=interval,  # Delay between frames in ms
            blit=False,
            repeat=repeat if file_path is None else False,
        )

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
                raise FileNotFoundError("Provided path does not exist")
            writer = None
            if file_path.endswith(".mp4"):
                writer = animation.FFMpegWriter(
                    fps=fps, metadata={"artist": "ezGPX"}, bitrate=bitrate
                )
            elif file_path.endswith(".gif"):
                writer = animation.PillowWriter(
                    fps=fps, metadata={"artist": "ezGPX"}, bitrate=bitrate
                )
            ani.save(file_path, writer=writer)

        return fig
