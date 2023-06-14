import pandas as pd
import matplotlib.pyplot as plt

import logging

from ..gpx_elements import Gpx
from ..gpx_parser import Parser
from ..gpx_writer import Writer

class GPX():
    """
    High level GPX object.
    """
    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.parser: Parser = Parser(file_path)
        self.gpx: Gpx = self.parser.gpx
        self.writer: Writer = Writer()

    def nb_points(self):
        """
        Compute the number of points in the GPX.

        Returns:
            int: Number of points in the GPX.
        """
        nb_pts = 0
        for track in self.gpx.tracks:
            for track_segment in track.track_segments:
                nb_pts += len(track_segment.track_points)
        return nb_pts
    
    def distance(self):
        """
        Returns the distance (meters) of the tracks contained in the GPX.

        Returns:
            float: Distance (meters).
        """
        return self.gpx.distance()

    def to_string(self) -> str:
        return self.writer.gpx_to_string(self.gpx)

    def to_gpx(self, path: str):
        self.writer.write(self.gpx, path)

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
        self.gpx.remove_gps_errors()

    def compress(self, compression_method: str = "Ramer-Douglas-Peucker algorithm"):
        """
        Compress GPX by removing points.

        Args:
            compression_method (str, optional): Method used to compress GPX. Defaults to "Ramer-Douglas-Peucker algorithm".
        """
        if compression_method == "Ramer-Douglas-Peucker algorithm":
            logging.debug("Ramer-Douglas-Peucker algorithm is not implemented yet")
            pass
        elif compression_method == "Remove 25% points":
            self.gpx.remove_points(4)
        elif compression_method == "Remove 50% points":
            self.gpx.remove_points(2)
        elif compression_method == "Remove 75% points":
            pass
        elif compression_method == "Remove elevation":
            logging.debug("Removing elevation is not implemented yet")

    def plot(self, title: str = "Track", base_color: str = "#101010", start_stop: bool = False, elevation_color: bool = False, file_path: str = None,):

        # Create dataframe containing data from the GPX file
        gpx_df = self.to_dataframe()

        # Visualize GPX file
        plt.figure(figsize=(14, 8))
        if elevation_color:
            plt.scatter(gpx_df["longitude"], gpx_df["latitude"], c=gpx_df["elevation"])
        else:
            plt.scatter(gpx_df["longitude"], gpx_df["latitude"], color=base_color)
        
        if start_stop:
            plt.scatter(gpx_df["longitude"][0], gpx_df["latitude"][0], color="#00FF00")
            plt.scatter(gpx_df["longitude"][len(gpx_df["longitude"])-1], gpx_df["latitude"][len(gpx_df["longitude"])-1], color="#FF0000")
        
        plt.title(title, size=20)
        plt.xticks([min(gpx_df["longitude"]), max(gpx_df["longitude"])])
        plt.yticks([min(gpx_df["latitude"]), max(gpx_df["latitude"])])


        if file_path is not None:
            # Check path
            plt.savefig(file_path)
        else:
            plt.show()