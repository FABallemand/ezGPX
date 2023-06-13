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
    
    # def removeGPSErrors(gpx, error_distance=1000):
    #     """
    #     Remove GPS errors.

    #     Args:
    #         gpx (GPX): GPX object.
    #         error_distance (int, optional): GPS error threshold distance (in meters) between two points. Defaults to 1000.

    #     Returns:
    #         GPX: GPX object without GPS error.
    #         list: List of removed points (GPS errors).
    #     """
    #     # Create new "file"
    #     cleaned_gpx = gpxpy.gpx.GPX()

    #     previous_point = None
    #     GPS_errors = []

    #     for track in gpx.tracks:
    #         # Create track
    #         gpx_track = gpxpy.gpx.GPXTrack()
    #         cleaned_gpx.tracks.append(gpx_track)
    #         for segment in track.segments:
    #             # Create segment
    #             gpx_segment = gpxpy.gpx.GPXTrackSegment()
    #             gpx_track.segments.append(gpx_segment)
    #             for point in segment.points:
    #                 # Create points
    #                 if previous_point is None or gpxpy.geo.haversine_distance(previous_point.latitude,
    #                                                                         previous_point.longitude,
    #                                                                         point.latitude,
    #                                                                         point.longitude) < error_distance:
    #                     gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point.latitude, point.longitude, elevation=point.elevation))
    #                     previous_point = point
    #                 else:
    #                     GPS_errors.append(point)
    #     return cleaned_gpx, GPS_errors

    # def compressFile(gpx, compression_method="Ramer-Douglas-Peucker algorithm", vertical_smooth=True, horizontal_smooth=True):
    #     """
    #     Compress GPX file.

    #     Args:
    #         gpx (GPX): GPX object.
    #         compression_method (str, optional): Method used to compress GPX. Defaults to "RPD".
    #         vertical_smooth (bool, optional): Vertical smoothing. Defaults to True.
    #         horizontal_smooth (bool, optional): Horizontal smoothing. Defaults to True.

    #     Returns:
    #         GPX: Compressed GPX object.
    #     """
    #     # Smoothing
    #     gpx.smooth(vertical=vertical_smooth, horizontal=horizontal_smooth)

    #     # Compression
    #     if compression_method == "Ramer-Douglas-Peucker algorithm":
    #         gpx.simplify()
    #     elif compression_method == "Remove 25% points":
    #         gpx.reduce_points(int(gpx.get_track_points_no() * 0.75))
    #     elif compression_method == "Remove 50% points":
    #         gpx.reduce_points(int(gpx.get_track_points_no() * 0.5))
    #     elif compression_method == "Remove 75% points":
    #         gpx.reduce_points(int(gpx.get_track_points_no() * 0.25))
            
    #     return gpx

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