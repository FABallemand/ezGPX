import logging
import webbrowser
from datetime import datetime
import pandas as pd
from math import degrees

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

import gmplot

import folium
from folium.plugins import MiniMap
from folium.features import DivIcon

from ..gpx_elements import Gpx, WayPoint
from ..gpx_parser import Parser
from ..gpx_writer import Writer
from ..utils import EARTH_RADIUS

class GPX():
    """
    High level GPX object.
    """

    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.parser: Parser = Parser(file_path)
        self.gpx: Gpx = self.parser.gpx
        self.writer: Writer = Writer(self.gpx, precisions=self.parser.precisions, time_format=self.parser.time_format)

    def name(self) -> str:
        """
        Return activity name.

        Returns:
            str: Activity name.
        """
        return self.gpx.name()

    def nb_points(self) -> int:
        """
        Return the number of points in the GPX.

        Returns:
            int: Number of points in the GPX.
        """
        return self.gpx.nb_points()
    
    def first_point(self) -> WayPoint:
        """
        Return GPX first point.

        Returns:
            WayPoint: First point.
        """
        return self.gpx.tracks[0].trkseg[0].trkpt[0]
    
    def last_point(self) -> WayPoint:
        """
        Return GPX last point.

        Returns:
            WayPoint: Last point.
        """
        return self.gpx.tracks[-1].trkseg[-1].trkpt[-1]
    
    def bounds(self) -> tuple[float, float, float, float]:
        """
        Find minimum and maximum latitude and longitude.

        Returns:
            tuple[float, float, float, float]: Min latitude, min longitude, max latitude, max longitude
        """
        return self.gpx.bounds()
    
    def center(self) -> tuple[float, float]:
        """
        Return the coordinates of the center point.

        Returns:
            tuple[float, float]: Latitude and longitude of the center point.
        """
        return self.gpx.center()
    
    def distance(self) -> float:
        """
        Returns the distance (meters) of the tracks contained in the GPX.

        Returns:
            float: Distance (meters).
        """
        return self.gpx.distance()
    
    def ascent(self) -> float:
        """
        Returns the ascent (meters) of the tracks contained in the GPX.

        Returns:
            float: Ascent (meters).
        """
        return self.gpx.ascent()
    
    def descent(self) -> float:
        """
        Returns the descent (meters) of the tracks contained in the GPX.

        Returns:
            float: Descent (meters).
        """
        return self.gpx.descent()

    def min_elevation(self) -> float:
        """
        Returns the minimum elevation (meters) in the tracks contained in the GPX.

        Returns:
            float: Minimum elevation (meters).
        """
        return self.gpx.min_elevation()
    
    def max_elevation(self) -> float:
        """
        Returns the maximum elevation (meters) in the tracks contained in the GPX.

        Returns:
            float: Maximum elevation (meters).
        """
        return self.gpx.max_elevation()
    
    def start_time(self) -> datetime:
        """
        Return the activity start time.

        Returns:
            datetime: Start time.
        """
        return self.gpx.start_time()
    
    def stop_time(self) -> datetime:
        """
        Return the activity stop time.

        Returns:
            datetime: Stop time.
        """
        return self.gpx.stop_time()
    
    def total_elapsed_time(self) -> datetime:
        """
        Return the total elapsed time during the activity.

        Returns:
            datetime: Total elapsed time.
        """
        return self.gpx.total_elapsed_time()
    
    def stopped_time(self) -> datetime:
        """
        Return the stopped time during the activity.

        Returns:
            datetime: Stopped time.
        """
        return self.gpx.stopped_time()
    
    def moving_time(self) -> datetime:
        """
        Return the moving time during the activity.

        Returns:
            datetime: Moving time.
        """
        return self.gpx.moving_time()
    
    def avg_speed(self) -> float:
        """
        Return average speed (kilometers per hour) during the activity.

        Returns:
            float: Average speed (kilometers per hour).
        """
        return self.gpx.avg_speed()
    
    def avg_moving_speed(self) -> float:
        """
        Return average moving speed (kilometers per hour) during the activity.

        Returns:
            float: Average moving speed (kilometers per hour).
        """
        return self.gpx.avg_moving_speed()
    
    def max_speed(self) -> float:
        # TODO
        pass

    def avg_pace(self) -> float:
        """
        Return average pace (minutes per kilometer) during the activity.

        Returns:
            float: Average pace (minutes per kilometer).
        """
        return self.gpx.avg_pace()
    
    def avg_moving_pace(self) -> float:
        """
        Return average moving pace (minutes per kilometer) during the activity.

        Returns:
            float: Average moving pace (minutes per kilometer).
        """
        return self.gpx.avg_moving_pace()

    def to_string(self) -> str:
        """
        Convert the GPX object to a string.

        Returns:
            str: String representingth GPX object.
        """
        return self.writer.gpx_to_string(self.gpx)

    def to_gpx(self, path: str):
        """
        Write the GPX object to a .gpx file.

        Args:
            path (str): Path to the .gpx file.
        """
        self.writer.write(path)

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert GPX object to Pandas Dataframe.

        Returns:
            pd.DataFrame: Dataframe containing position data from GPX.
        """
        return self.gpx.to_dataframe()
    
    def remove_metadata(self):
        """
        Remove metadata (ie: metadata will not be written when saving the GPX object as a .gpx file).
        """
        self.writer.metadata = False
    
    def remove_elevation(self):
        """
        Remove elevation data (ie: elevation data will not be written when saving the GPX object as a .gpx file).
        """
        self.writer.ele = False

    def remove_time(self):
        """
        Remove time data (ie: time data will not be written when saving the GPX object as a .gpx file).
        """
        self.writer.time = False
    
    def remove_gps_errors(self):
        """
        Remove GPS errors.
        """
        self.gpx.remove_gps_errors()

    def remove_close_points(self, min_dist: float = 1, max_dist: float = 10):
        """
        Remove points that are to close together.

        Args:
            min_dist (float, optional): Minimal distance between two points. Defaults to 1.
            max_dist (float, optional): Maximal distance between two points. Defaults to 10.
        """
        self.gpx.remove_close_points(min_dist, max_dist)

    def simplify(self, tolerance: float = 2):
        """
        Simplify the tracks using Ramer-Douglas-Peucker algorithm.

        Args:
            tolerance (float, optional): Tolerance (meters). Corresponds to the
            minimum distance between the point and the track before the point
            is removed. Defaults to 2.
        """
        epsilon = degrees(tolerance/EARTH_RADIUS)
        self.gpx.simplify(epsilon)

    def matplotlib_plot(
            self,
            projection: str = None,
            title: str = "Track",
            base_color: str = "#101010",
            start_stop: bool = False,
            way_points: bool = False,
            elevation_color: bool = False,
            duration: bool = False,
            distance: bool = False,
            ascent: bool = False,
            pace: bool = False,
            speed: bool = False,
            file_path: str = None):
        """
        Plot GPX using Matplotlib.

        Args:
            projection (str, optional): Projection to use. Defaults to None.
            title (str, optional): Title. Defaults to "Track".
            base_color (str, optional): Track color. Defaults to "#101010".
            start_stop (bool, optional): Plot start and stop points in green and red. Defaults to False.
            way_points (bool, optional): Plot way points in blue. Defaults to False.
            elevation_color (bool, optional): Plot track with color according to elevation. Defaults to False.
            duration (bool, optional): Display duration. Defaults to False.
            distance (bool, optional): Display distance. Defaults to False.
            ascent (bool, optional): Display ascent. Defaults to False.
            pace (bool, optional): Display pace. Defaults to False.
            speed (bool, optional): Display pace. Defaults to False.
            file_path (str, optional): Path to save plot. Defaults to None.
        """
        # Handle projection
        if projection is None:
            column_x = "longitude"
            column_y = "latitude"
        else:
            # Select dataframe columns to use
            column_x = "x"
            column_y = "y"
            # Project
            self.gpx.project(projection)

        # Create dataframe containing data from the GPX file
        gpx_df = self.to_dataframe()

        # Visualize GPX file
        fig = plt.figure(figsize=(14, 8))
        if elevation_color:
            plt.scatter(gpx_df[column_x], gpx_df[column_y], c=gpx_df["elevation"])
        else:
            plt.scatter(gpx_df[column_x], gpx_df[column_y], color=base_color)
        
        if start_stop:
            plt.scatter(gpx_df[column_x][0], gpx_df[column_y][0], color="#00FF00")
            plt.scatter(gpx_df[column_x][len(gpx_df[column_x])-1], gpx_df[column_y][len(gpx_df[column_x])-1], color="#FF0000")
        if way_points:
            for way_point in self.gpx.wpt:
                if projection:
                    way_point.project(projection)
                    plt.scatter(way_point._x, way_point._y, color="#0000FF")
                else:
                    plt.scatter(way_point.lon, way_point.lat, color="#0000FF")
        
        text_kwargs = dict(ha='center', va='center', fontsize=10, transform=fig.axes[0].transAxes, bbox=dict(facecolor='gray', alpha=0.5))

        if duration:
            plt.text(0, 0, f"Duration:\n{self.total_elapsed_time()}", **text_kwargs)

        if distance:
            plt.text(0.5, 0, f"Distance:\n{self.distance()/1000:.2f} km", **text_kwargs)

        if ascent:
            plt.text(1, 0, f"Ascent:\n{self.ascent():.2f} m", **text_kwargs)
        elif pace:
            plt.text(1, 0, f"Pace:\n{self.avg_pace():.2f} min/km", **text_kwargs)
        elif speed:
            plt.text(1, 0, f"Speed:\n{self.avg_speed():.2f} km/h", **text_kwargs)

        plt.title(title, size=20)
        plt.xticks([min(gpx_df[column_x]), max(gpx_df[column_x])])
        plt.yticks([min(gpx_df[column_y]), max(gpx_df[column_y])])
        
        if projection is not None:
            ax = plt.gca()
            ax.set_xlim(left=min(gpx_df[column_x]), right=max(gpx_df[column_x]))
            ax.set_ylim(bottom=min(gpx_df[column_y]), top=max(gpx_df[column_y]))

        if file_path is not None:
            # Check path
            plt.savefig(file_path)
        else:
            plt.show()

    def matplotlib_basemap_plot(
            self,
            projection: str = "cyl",
            title: str = "Track",
            base_color: str = "#101010",
            start_stop: bool = False,
            way_points: bool = False,
            duration: bool = False,
            distance: bool = False,
            ascent: bool = False,
            pace: bool = False,
            speed: bool = False,
            file_path: str = None):
        """
        Plot GPX using Matplotlib Basemap Toolkit.

        Args:
            projection (str, optional): Projection. Defaults to "cyl".
            title (str, optional): Title. Defaults to "Track".
            base_color (str, optional): Track color. Defaults to "#101010".
            start_stop (bool, optional): Plot start and stop points in green and red. Defaults to False.
            way_points (bool, optional): Plot way points in blue. Defaults to False.
            duration (bool, optional): _description_. Defaults to False.
            distance (bool, optional): _description_. Defaults to False.
            ascent (bool, optional): _description_. Defaults to False.
            pace (bool, optional): _description_. Defaults to False.
            speed (bool, optional): _description_. Defaults to False.
            file_path (str, optional): _description_. Defaults to None.
        """
        fig = plt.figure(figsize=(14, 8))
        center_lat, center_lon = self.center()
        min_lat, min_lon, max_lat, max_lon = self.bounds()
        # offset = 0.1
        offset = 0.001
        min_lat, min_lon = max(0, min_lat - offset), max(0, min_lon - offset)
        max_lat, max_lon = min(max_lat + offset, 90), min(max_lon + offset, 90)

        map = Basemap(projection=projection,
                      llcrnrlon=min_lon,
                      llcrnrlat=min_lat,
                      urcrnrlon=max_lon,
                      urcrnrlat=max_lat)

        # map.drawmapboundary(fill_color='aqua')
        # map.fillcontinents(color='coral',lake_color='aqua')
        # map.drawcoastlines()

        # map.bluemarble()
        # map.shadedrelief()
        # map.etopo()
        map.arcgisimage(service='World_Shaded_Relief', xpixels = 1500, dpi=200, verbose= True)

        test_gpx_df = self.to_dataframe()
        x, y = map(test_gpx_df["longitude"], test_gpx_df["latitude"])
        x = x.tolist()
        y = y.tolist()
        map.plot(x, y, marker=None, color=base_color)

        if start_stop:
            map.plot(x[0], y[0], marker="^", color="#00FF00")
            map.plot(x[-1], y[-1], marker="h", color="#FF0000")
        if way_points:
            for way_point in self.gpx.wpt:
                x, y = map(way_point.lon, way_point.lat)
                map.plot(x, y, marker="D", color="#0000FF")

        text_kwargs = dict(ha='center', va='center', fontsize=10, transform=fig.axes[0].transAxes, bbox=dict(facecolor='gray', alpha=0.5))

        if duration:
            plt.text(0, 0, f"Duration:\n{self.total_elapsed_time()}", **text_kwargs)

        if distance:
            plt.text(0.5, 0, f"Distance:\n{self.distance()/1000:.2f} km", **text_kwargs)

        if ascent:
            plt.text(1, 0, f"Ascent:\n{self.ascent():.2f} m", **text_kwargs)
        elif pace:
            plt.text(1, 0, f"Pace:\n{self.avg_pace():.2f} min/km", **text_kwargs)
        elif speed:
            plt.text(1, 0, f"Speed:\n{self.avg_speed():.2f} km/h", **text_kwargs)

        plt.title(title, size=20)

        if file_path is not None:
            # Check path
            plt.savefig(file_path)
        else:
            plt.show()

    def gmap_plot(
        self,
        title: str = None,
        base_color: str = "#110000",
        start_stop: bool = False,
        way_points: bool = False,
        zoom: float = 10.0,
        file_path: str = None,
        open: bool = True,
        scatter: bool = False,
        plot: bool = True):
        """
        Plot GPX using gmap.

        Args:
            title (str, optional): Title. Defaults to None.
            base_color (str, optional): Track_color. Defaults to "#110000".
            start_stop (bool, optional): Plot start and stop points in green and red. Defaults to False.
            way_points (bool, optional): Plot way points in blue. Defaults to False.
            zoom (float, optional): Zoom. Defaults to 10.0.
            file_path (str, optional): Path to save plot. Defaults to None.
            open (bool, optional): Open the plot in the default web browser. Defaults to True.
            scatter (bool, optional): Scatter track points. Defaults to False.
            plot (bool, optional): Plot track points. Defaults to True.
        """
        # Convert to dataframe and compute center latitude and longitude
        test_gpx_df = self.to_dataframe()
        center_lat, center_lon = self.center()

        # Create plotter
        map = gmplot.GoogleMapPlotter(center_lat, center_lon, zoom)

        # Plot and save
        if title is not None:
            map.text(center_lat, center_lon, self.name(), color="#FFFFFF")
        if start_stop:
            map.scatter([self.gpx.tracks[0].trkseg[0].trkpt[0].lat], [self.gpx.tracks[0].trkseg[0].trkpt[0].lon], "#00FF00", size=5, marker=True)
            map.scatter([self.gpx.tracks[-1].trkseg[-1].trkpt[-1].lat], [self.gpx.tracks[-1].trkseg[-1].trkpt[-1].lon], "#FF0000", size=5, marker=True)
        if way_points:
            for way_point in self.gpx.wpt:
                map.scatter([way_point.lat], [way_point.lon], "#0000FF", size=5, marker=True)
        if scatter:
            map.scatter(test_gpx_df["latitude"], test_gpx_df["longitude"], base_color, size=5, marker=False)
        if plot:
            map.plot(test_gpx_df["latitude"], test_gpx_df["longitude"], base_color, edge_width=2.5)

        map.draw(file_path)

        # Open
        if open:
            webbrowser.open(file_path)

    def folium_plot(
            self,
            title: str = None,
            tiles: str = "OpenStreetMap", # "OpenStreetMap", "Stamen Terrain", "Stamen Toner"
            base_color: str = "#110000",
            start_stop: bool = False,
            way_points: bool = False,
            minimap: bool = False,
            coord_popup: bool = False,
            zoom: float = 12.0,
            file_path: str = None,
            open: bool = True):
        
        center_lat, center_lon = self.center()
        min_lat, min_lon, max_lat, max_lon = self.bounds()
        offset = 0.001
        min_lat, min_lon = max(0, min_lat - offset), max(0, min_lon - offset)
        max_lat, max_lon = min(max_lat + offset, 90), min(max_lon + offset, 90)

        # Create map
        m = folium.Map(location=[center_lat, center_lon],
                       zoom_start=zoom,
                       tiles=tiles)
        
        # Title
        if title is not None:
            folium.map.Marker(
                [center_lat, center_lon],   
                icon=DivIcon(
                    icon_size=(250,36),
                    icon_anchor=(0,0),
                    html=f'<div style="font-size: 20pt">{title}</div>',
                    )
                ).add_to(m)

        if start_stop:
            folium.Marker([self.gpx.tracks[0].trkseg[0].trkpt[0].lat, self.gpx.tracks[0].trkseg[0].trkpt[0].lon], popup="<b>Start</b>", tooltip="Start", icon=folium.Icon(color="green")).add_to(m)
            folium.Marker([self.gpx.tracks[-1].trkseg[-1].trkpt[-1].lat, self.gpx.tracks[-1].trkseg[-1].trkpt[-1].lon], popup="<b>Stop</b>", tooltip="Stop", icon=folium.Icon(color="red")).add_to(m)
        if way_points:
            for way_point in self.gpx.wpt:
                folium.Marker([way_point.lat, way_point.lon], popup="<i>Way point</i>", tooltip="Way point", icon=folium.Icon(icon="info-sign")).add_to(m)

        # Add latitude-longitude pop-up
        if coord_popup:
            m.add_child(folium.LatLngPopup())

        # Add minimap
        if minimap:
            minimap = MiniMap(toggle_display=True)
            minimap.add_to(m)

        # Plot
        test_gpx_df = self.to_dataframe()
        test_gpx_df["coordinates"] = list(zip(test_gpx_df.latitude, test_gpx_df.longitude))
        folium.PolyLine(test_gpx_df["coordinates"], tooltip=title, color=base_color).add_to(m)

        # Save map
        m.save(file_path)

        # Open map in web browser
        if open:
            webbrowser.open(file_path)