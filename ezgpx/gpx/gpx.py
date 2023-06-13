from typing import *
import pandas as pd
import matplotlib.pyplot as plt

from ..gpx_elements import Gpx
from ..gpx_parser import Parser
from ..gpx_writer import Writer

class GPX():
    """
    High level GPX object.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.parser = Parser(file_path)
        self.gpx = self.parser.gpx
        self.writer = Writer()

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