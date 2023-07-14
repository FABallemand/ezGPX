import logging
from datetime import datetime
import pandas as pd
from math import degrees

import matplotlib.pyplot as plt

import webbrowser
import gmplot

from ..gpx_elements import Gpx
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
            elevation_color: bool = False,
            duration: bool = False,
            distance: bool = False,
            ascent: bool = False,
            pace: bool = False,
            speed: bool = False,
            file_path: str = None):

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
            # plt.scatter(gpx_df[column_x][len(gpx_df[column_x])-2], gpx_df[column_y][len(gpx_df[column_x])-2], color="#0000FF")
            # plt.scatter(gpx_df[column_x][len(gpx_df[column_x])-3], gpx_df[column_y][len(gpx_df[column_x])-3], color="#FF00FF")

        
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

    def gmap_plot(
        self,
        title: str = None,
        base_color: str = "#110000",
        start_stop: str = False,
        zoom: float = 10.0,
        file_path: str = None,
        open: bool = True,
        scatter: bool = False,
        plot: bool = True):

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
            map.scatter([self.gpx.tracks[-1].trkseg[-1].trkpt[-1].lat], [self.gpx.tracks[-1].trkseg[-1].trkpt[-1].lat], "#FF0000", size=5, marker=True)
        if scatter:
            map.scatter(test_gpx_df["latitude"], test_gpx_df["longitude"], base_color, size=5, marker=False)
        if plot:
            map.plot(test_gpx_df["latitude"], test_gpx_df["longitude"], base_color, edge_width=2.5)
        map.draw(file_path)

        # Open
        if open:
            webbrowser.open(file_path)