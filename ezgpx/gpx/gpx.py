from datetime import datetime

import pandas as pd
from math import degrees
import matplotlib.pyplot as plt

import logging

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
        self.writer: Writer = Writer(self.gpx, precisions=self.parser.precisions)

    def nb_points(self) -> int:
        """
        Compute the number of points in the GPX.

        Returns:
            int: Number of points in the GPX.
        """
        nb_pts = 0
        for track in self.gpx.tracks:
            for track_segment in track.trkseg:
                nb_pts += len(track_segment.trkpt)
        return nb_pts
    
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
    
    def avg_speed(self) -> float:
        """
        Return average speed (kilometers per hour) during the activity.

        Returns:
            float: Average speed (kilometers per hour).
        """
        return self.gpx.avg_speed()

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

    def plot(
            self,
            projection: str = None,
            title: str = "Track",
            base_color: str = "#101010",
            start_stop: bool = False,
            elevation_color: bool = False,
            duration: bool = None,
            distance: bool = None,
            ascent: bool = None,
            pace: bool = None,
            speed: bool = None,
            file_path: str = None):

        # Handle projection
        if projection in ["Web Mercator"]:
            logging.info("-> Handling projection")
            # Project points
            self.gpx.project()

            # Select dataframe columns to use
            column_x = "x"
            column_y = "y"
        else:
            column_x = "longitude"
            column_y = "latitude"

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
        
        text_kwargs = dict(ha='center', va='center', fontsize=10, transform=fig.axes[0].transAxes)

        if duration:
            plt.text(0, 0, f"Duration:\n{self.total_elapsed_time()}", **text_kwargs)

        if distance:
            plt.text(0.5, 0, f"Distance:\n{self.distance()/1000:.2f} km", **text_kwargs)

        if ascent:
            plt.text(1, 0, f"Ascent:\n{self.ascent():.2f} m", **text_kwargs)
        elif pace:
            # plt.text(1, 0, f"Pace:\n{self.pace()}", **text_kwargs)
            pass
        elif speed:
            plt.text(1, 0, f"Speed:\n{self.avg_speed():.2f} km/h", **text_kwargs)

        plt.title(title, size=20)
        plt.xticks([min(gpx_df[column_x]), max(gpx_df[column_x])])
        plt.yticks([min(gpx_df[column_y]), max(gpx_df[column_y])])


        if file_path is not None:
            # Check path
            plt.savefig(file_path)
        else:
            plt.show()