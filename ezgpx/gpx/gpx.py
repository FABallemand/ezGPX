import os
from typing import Optional, Union, List, Tuple, Dict, NewType
import logging
from zipfile import ZipFile
import webbrowser
from datetime import datetime
from math import degrees, isclose
import pandas as pd
import numpy as np

from fitparse import FitFile

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
import matplotlib.animation as animation

import gmplot

import folium
from folium.plugins import MiniMap
from folium.features import DivIcon

from papermap import PaperMap

from ..gpx_elements import Gpx, WayPoint
from ..gpx_parser import GPXParser
from ..kml_parser import KMLParser
from ..fit_parser import FitParser
from ..gpx_writer import GPXWriter
from ..kml_writer import KMLWriter
from ..utils import haversine_distance, EARTH_RADIUS

GPX = NewType("GPX", object) # GPX forward declaration for type hint

class GPX():
    """
    High level GPX object.
    """

    def __init__(
            self,
            file_path: Optional[str] = None,
            xml_schema: bool = True,
            xml_extensions_schemas: bool = False) -> None:
        """
        Initialise GPX instance.

        Parameters
        ----------
        file_path : Optional[str], optional
            Path to the file to parse, by default None
        xml_schema : bool, optional
            Toggle schema verification during parsing, by default True
        extensions_schemas : bool, optional
            Toggle extensions schema verificaton during parsing, by default False
        """
        if file_path is not None and os.path.exists(file_path):
            self.file_path: str = file_path
            self.file_name: str = os.path.basename(file_path)
            self.gpx: Gpx = None
            self.gpx_parser: GPXParser = None
            self.kml_parser: KMLParser = None
            self.fit_parser: FitParser = None
            self.precisions: Dict = None
            self.time_data: bool = False
            self.time_format: str = None
            self.dataframe: pd.DataFrame = None

            # GPX
            if file_path.endswith(".gpx"):
                self.gpx_parser = GPXParser(file_path, xml_schema, xml_extensions_schemas)
                self.gpx = self.gpx_parser.gpx
                self.precisions = self.gpx_parser.precisions
                self.time_data = self.gpx_parser.time_data
                self.time_format = self.gpx_parser.time_format

            # KML
            elif file_path.endswith(".kml"):
                self.kml_parser = KMLParser(file_path, xml_schema, xml_extensions_schemas)
                self.gpx = self.kml_parser.gpx
                self.precisions = self.kml_parser.precisions
                self.time_format = self.kml_parser.time_format

            # KMZ
            elif file_path.endswith(".kmz"):
                kmz = ZipFile(file_path, 'r')
                kmls = [info.filename for info in kmz.infolist() if info.filename.endswith(".kml")]
                if "doc.kml" not in kmls:
                    logging.warning("Unable to parse this file: Expected to find doc.kml inside KMZ file.")
                kml = kmz.open("doc.kml", 'r').read()
                self.write_tmp_kml("tmp.kml", kml)
                self.kml_parser = KMLParser("tmp.kml", xml_schema, xml_extensions_schemas)
                self.gpx = self.kml_parser.gpx
                self.precisions = self.kml_parser.precisions
                self.time_format = self.kml_parser.time_format
                os.remove("tmp.kml")
            
            # FIT
            elif file_path.endswith(".fit"):
                self.fit_parser = FitParser(file_path)
                self.gpx = self.fit_parser.gpx
                self.precisions = self.fit_parser.precisions
                self.time_format = self.fit_parser.time_format

            # NOT SUPPORTED
            else:
                logging.error("Unable to parse this type of file...\nYou may consider renaming your file with the proper file extension.")
            self.gpx_writer: GPXWriter = GPXWriter(
                self.gpx, precisions=self.precisions, time_format=self.time_format)
            self.kml_writer: KMLWriter = KMLWriter(
                self.gpx, precisions=self.precisions, time_format=self.time_format)
        else:
            logging.warning("File path does not exist")
            pass

    def write_tmp_kml(
            self,
            path: str ="tmp.kml",
            kml_string: Optional[bytes] = None):
        """
        Write temproray .KML file in order to parse KMZ file.
        """
        # Open/create KML file
        try:
            f = open(path, "wb")
        except OSError:
            logging.exception(f"Could not open/read file: {path}")
            raise
        # Write KML file
        with f:
            if kml_string is not None:
                f.write(kml_string)

    def __str__(self) -> str:
        return f"file_path = {self.file_path}\ngpx = {self.gpx}"
    
###############################################################################
#### Schemas ##################################################################
###############################################################################
    
    def check_xml_schema(self) -> bool:
        """
        Check XML schema.

        Returns
        -------
        bool
            True if the file follows XML schemas.
        """
        return self.gpx.check_xml_schema(self.file_path)
    
    def check_xml_extensions_schemas(self) -> bool:
        """
        Check XML extension schemas.

        Returns
        -------
        bool
            True if the file follows XML schemas.
        """
        return self.gpx.check_xml_extensions_schemas(self.file_path)
    
###############################################################################
#### Name #####################################################################
###############################################################################
        
    def file_name(self) -> Union[str, None]:
        """
        Return .gpx file name.

        Returns
        -------
        Union[str, None]
            File name.
        """
        return os.path.basename(self.file_path)

    def name(self) -> str:
        """
        Return activity name.

        Returns
        -------
        str
            Activity name.
        """
        return self.gpx.name()
    
    def set_name(self, new_name: str) -> None:
        """
        Set name.

        Parameters
        ----------
        new_name : str
            New name.
        """
        self.gpx.set_name(new_name)

###############################################################################
#### Points ###################################################################
###############################################################################

    def nb_points(self) -> int:
        """
        Return the number of points in the GPX.

        Returns
        -------
        int
            Number of points in the GPX.
        """
        return self.gpx.nb_points()

    def first_point(self) -> WayPoint:
        """
        Return GPX first point.

        Returns
        -------
        WayPoint
            First point.
        """
        return self.gpx.first_point()

    def last_point(self) -> WayPoint:
        """
        Return GPX last point.

        Returns
        -------
        WayPoint
            Last point.
        """
        return self.gpx.last_point()

    def bounds(self) -> Tuple[float, float, float, float]:
        """
        Find minimum and maximum latitude and longitude.

        Returns
        -------
        Tuple[float, float, float, float]
            Min latitude, min longitude, max latitude, max longitude.
        """
        return self.gpx.bounds()

    def center(self) -> Tuple[float, float]:
        """
        Return the coordinates of the center point.

        Returns
        -------
        Tuple[float, float]
            Latitude and longitude of the center point.
        """
        return self.gpx.center()
    
    def extreme_points(self) -> Tuple[WayPoint, WayPoint, WayPoint, WayPoint]:
        """
        Find extreme points in track, i.e.: points with lowest and highest latitude and longitude.

        Returns
        -------
        Tuple[WayPoint, WayPoint, WayPoint, WayPoint]
            Min latitude point, min longitude point, max latitude point, max longitude point
        """
        return self.gpx.extreme_points()
    
###############################################################################
#### Distance and Elevation ###################################################
###############################################################################

    def distance(self) -> float:
        """
        Returns the distance (meters) of the tracks contained in the GPX.

        Returns
        -------
        float
            Distance (meters).
        """
        return self.gpx.distance()

    def ascent(self) -> float:
        """
        Returns the ascent (meters) of the tracks contained in the GPX.

        Returns
        -------
        float
            Ascent (meters).
        """
        return self.gpx.ascent()

    def descent(self) -> float:
        """
        Returns the descent (meters) of the tracks contained in the GPX.

        Returns
        -------
        float
            Descent (meters).
        """
        return self.gpx.descent()
    
    def compute_points_ascent_rate(self) -> None:
        """
        Compute ascent rate at each point.
        """
        self.gpx.compute_points_ascent_rate()

    def min_ascent_rate(self) -> float:
        """
        Return activity minimum ascent rate.

        Returns
        -------
        float
            Minimum ascent rate.
        """
        return self.gpx.min_ascent_rate()
    
    def max_ascent_rate(self) -> float:
        """
        Return activity maximum ascent rate.

        Returns
        -------
        float
            Maximum ascent rate.
        """
        return self.gpx.max_ascent_rate()

    def min_elevation(self) -> float:
        """
        Returns the minimum elevation (meters) in the tracks contained in the GPX.

        Returns
        -------
        float
            Minimum elevation (meters).
        """
        return self.gpx.min_elevation()

    def max_elevation(self) -> float:
        """
        Returns the maximum elevation (meters) in the tracks contained in the GPX.

        Returns
        -------
        float
            Maximum elevation (meters).
        """
        return self.gpx.max_elevation()
    
###############################################################################
#### Time #####################################################################
###############################################################################

    def start_time(self) -> datetime:
        """
        Return the activity start time.

        Returns
        -------
        datetime
            Start time.
        """
        return self.gpx.start_time()

    def stop_time(self) -> datetime:
        """
        Return the activity stop time.

        Returns
        -------
        datetime
            Stop time.
        """
        return self.gpx.stop_time()

    def total_elapsed_time(self) -> datetime:
        """
        Return the total elapsed time during the activity.

        Returns
        -------
        datetime
            Total elapsed time.
        """
        return self.gpx.total_elapsed_time()

    def stopped_time(self) -> datetime:
        """
        Return the stopped time during the activity.

        Returns
        -------
        datetime
            Stopped time.
        """
        return self.gpx.stopped_time()

    def moving_time(self) -> datetime:
        """
        Return the moving time during the activity.

        Returns
        -------
        datetime
            Moving time.
        """
        return self.gpx.moving_time()
    
###############################################################################
#### Speed and Pace ###########################################################
###############################################################################

    def avg_speed(self) -> float:
        """
        Return average speed (kilometers per hour) during the activity.

        Returns
        -------
        float
            Average speed (kilometers per hour).
        """
        return self.gpx.avg_speed()

    def avg_moving_speed(self) -> float:
        """
        Return average moving speed (kilometers per hour) during the activity.

        Returns
        -------
        float
            Average moving speed (kilometers per hour).
        """
        return self.gpx.avg_moving_speed()
    
    def compute_points_speed(self) -> None:
        """
        Compute speed (kilometers per hour) at each track point.
        """
        self.gpx.compute_points_speed()

    def min_speed(self) -> float:
        """
        Return the minimum speed during the activity.

        Returns
        -------
        float
            Minimum speed.
        """
        return self.gpx.min_speed()

    def max_speed(self) -> float:
        """
        Return the maximum speed during the activity.

        Returns
        -------
        float
            Maximum speed.
        """
        return self.gpx.max_speed()
    
    def avg_pace(self) -> float:
        """
        Return average pace (minutes per kilometer) during the activity.

        Returns
        -------
        float
            Average pace (minutes per kilometer).
        """
        return self.gpx.avg_pace()

    def avg_moving_pace(self) -> float:
        """
        Return average moving pace (minutes per kilometer) during the activity.

        Returns
        -------
        float
            Average moving pace (minutes per kilometer).
        """
        return self.gpx.avg_moving_pace()
    
    def compute_points_pace(self) -> None:
        """
        Compute pace at each track point.
        """
        self.gpx.compute_points_pace()

    def min_pace(self) -> float:
        """
        Return the minimum pace during the activity.

        Returns
        -------
        float
            Minimum pace.
        """
        return self.gpx.min_pace()

    def max_pace(self) -> float:
        """
        Return the maximum pace during the activity.

        Returns
        -------
        float
            Maximum pace.
        """
        return self.gpx.max_pace()
    
    def compute_points_ascent_speed(self) -> None:
        """
        Compute ascent speed (kilometers per hour) at each track point.
        """
        self.gpx.compute_points_ascent_speed()

    def min_ascent_speed(self) -> float:
        """
        Return the minimum ascent speed (kilometers per hour) during the activity.

        Returns
        -------
        float
            Minimum ascent speed.
        """
        return self.gpx.min_ascent_speed()

    def max_ascent_speed(self) -> float:
        """
        Return the maximum ascent speed (kilometers per hour) during the activity.

        Returns
        -------
        float
            Maximum ascent speed.
        """
        return self.gpx.max_ascent_speed()
    
###############################################################################
#### Data Removal #############################################################
###############################################################################

    def remove_metadata(self):
        """
        Remove metadata (ie: metadata will not be written when saving the GPX object as a .gpx file).
        """
        self.gpx_writer.metadata = False

    def remove_elevation(self):
        """
        Remove elevation data (ie: elevation data will not be written when saving the GPX object as a .gpx file).
        """
        self.gpx_writer.ele = False

    def remove_time(self):
        """
        Remove time data (ie: time data will not be written when saving the GPX object as a .gpx file).
        """
        self.gpx_writer.time = False

###############################################################################
#### Error Correction #########################################################
###############################################################################

    def remove_gps_errors(self):
        """
        Remove GPS errors.
        """
        self.gpx.remove_gps_errors()

    def remove_close_points(self, min_dist: float = 1, max_dist: float = 10):
        """
        Remove points that are to close together.

        Parameters
        ----------
        min_dist : float, optional
            Minimal distance between two points, by default 1
        max_dist : float, optional
            Maximal distance between two points, by default 10
        """
        self.gpx.remove_close_points(min_dist, max_dist)

###############################################################################
#### ... ######################################################################
###############################################################################

    def simplify(self, tolerance: float = 2):
        """
        Simplify the tracks using Ramer-Douglas-Peucker algorithm.

        Parameters
        ----------
        tolerance : float, optional
            Tolerance (meters). Corresponds to the minimum distance between the
            point and the track before the point is removed, by default 2
        """
        epsilon = degrees(tolerance/EARTH_RADIUS)
        self.gpx.simplify(epsilon)

    def merge(self, gpx: GPX):
        """
        _summary_

        Parameters
        ----------
        gpx : GPX
            _description_
        """
        # TODO
        if self.gpx.tag is None:
            self.gpx.tag = gpx.gpx.tag
        if self.gpx.creator is None:
            self.gpx.creator = gpx.gpx.creator
        if self.gpx.xmlns is None:
            self.gpx.xmlns = gpx.gpx.xmlns
        if self.gpx.version is None:
            self.gpx.version = gpx.gpx.version
        if self.gpx.xmlns_xsi is None:
            self.gpx.xmlns_xsi = gpx.gpx.xmlns_xsi
        self.gpx.xsi_schema_location.extend(gpx.gpx.xsi_schema_location)
        if self.gpx.xmlns_gpxtpx is None:
            self.gpx.xmlns_gpxtpx = gpx.gpx.xmlns_gpxtpx
        if self.gpx.xmlns_gpxx is None:
            self.gpx.xmlns_gpxx = gpx.gpx.xmlns_gpxx
        if self.gpx.xmlns_gpxtrk is None:
            self.gpx.xmlns_gpxtrk = gpx.gpx.xmlns_gpxtrk
        if self.gpx.xmlns_wptx1 is None:
            self.gpx.xmlns_wptx1 = gpx.gpx.xmlns_wptx1
        if self.gpx.metadata is None:
            self.gpx.metadata = gpx.gpx.metadata
        self.gpx.wpt.extend(gpx.gpx.wpt)
        self.gpx.rte.extend(gpx.gpx.rte)
        self.gpx.tracks.extend(gpx.gpx.tracks)
        if self.gpx.extensions is None:
            self.gpx.extensions = gpx.gpx.extensions

###############################################################################
#### Exports ##################################################################
###############################################################################

    def to_gpx_string(self) -> str:
        """
        Convert the GPX object to a string.

        Returns
        -------
        str
            String representingth GPX object.
        """
        return self.gpx_writer.gpx_to_string(self.gpx)
    
    def to_dataframe(
            self,
            elevation: bool = True,
            time: bool = True,
            speed: bool = False,
            pace: bool = False,
            ascent_rate: bool = False,
            ascent_speed: bool = False,
            distance_from_start: bool = False) -> pd.DataFrame:
        """
        Convert GPX object to Pandas Dataframe.

        Parameters
        ----------
        elevation : bool, optional
            Toggle elevation, by default True
        time : bool, optional
            Toggle time, by default False
        speed : bool, optional
            Toggle speed, by default False
        pace : bool, optional
            Toggle pace, by default False
        ascent_rate : bool, optional
            Toggle ascent rate, by default False
        ascent_speed : bool, optional
            Toggle ascent speed, by default False
        distance_from_start : bool, optional
            Toggle distance from start, by default False

        Returns
        -------
        pd.DataFrame
            Dataframe containing data from GPX.
        """
        # Disable time related values if no time data available
        if not self.time_data:
            time = False
            speed = False
            pace = False
            ascent_speed = False
        return self.gpx.to_dataframe(elevation,
                                     time,
                                     speed,
                                     pace,
                                     ascent_rate,
                                     ascent_speed,
                                     distance_from_start)

    def to_csv(
            self,
            path: str = None,
            sep: str = ",",
            columns: List[str] = None,
            header: bool = True,
            index: bool = False) -> Union[str, None]:
        """
        Write the GPX object track coordinates to a .csv file.

        Parameters
        ----------
        path : str, optional
            Path to the .csv file, by default None
        sep : str, optional
            Separator, by default ","
        columns : List[str], optional
            List of columns to write, by default None
        header : bool, optional
            Toggle header, by default True
        index : bool, optional
             Toggle index, by default False

        Returns
        -------
        str
            CSV like string if path is set to None.
        """
        return self.gpx.to_csv(path, sep, columns, header, index)
    
    def to_gpx(
            self,
            path: str,
            xml_schema: bool = True,
            xml_extensions_schemas: bool = False) -> bool:
        """
        Write the GPX object to a .gpx file.

        Parameters
        ----------
        path : str
            Path to the .gpx file.
        xml_schema : bool, optional
            Toggle schema verification after writting, by default True
        xml_extensions_schemas : bool, optional
            Toggle extensions schema verificaton after writing. Requires internet connection and is not guaranted to work, by default False

        Returns
        -------
        bool
            Return False if written file does not follow checked schemas. Return True otherwise.
        """
        return self.gpx_writer.write(path, xml_schema, xml_extensions_schemas)
    
    def to_kml(
            self,
            path: str,
            styles: Optional[List[Tuple[str, Dict]]] = None,
            xml_schema: bool = True) -> bool:
        """
        Write the GPX object to a .kml file.

        Parameters
        ----------
        path : str
            Path to the .gpx file.
        styles : List[Tuple[str, Dict]], optional
            List of (style_id, style) tuples, by default None
        xml_schema : bool, optional
            Toggle schema verification after writting, by default True

        Returns
        -------
        bool
            Return False if written file does not follow checked schemas. Return True otherwise.
        """
        return self.kml_writer.write(path, styles, xml_schema)
    
###############################################################################
#### Matplotlib Plot ##########################################################
###############################################################################

    def _broken_matplotlib_plot_(
            self,
            figsize: Tuple[int, int] = (16, 9),
            size: float = 10,
            color: str = "#101010",
            cmap: Optional[mpl.colors.Colormap] = None,
            colorbar: bool = False,
            start_point_color: Optional[str] = None,
            stop_point_color: Optional[str] = None,
            way_points_color: Optional[str] = None,
            background: Optional[str] = None,
            offset_percentage: float = 0.04,
            xpixels: int = 400,
            ypixels: Optional[int] = None,
            dpi: int = 96,
            title: Optional[str] = None,
            title_fontsize: int = 20,
            watermark: bool = False,
            file_path: str = None):
        # Create dataframe containing data from the GPX file
        self.dataframe = self.to_dataframe(projection=True,
                                           elevation=True,
                                           speed=True,
                                           pace=True,
                                           ascent_rate=True,
                                           ascent_speed=True,
                                           distance_from_start=True)

        # Create figure and axes
        fig, ax = plt.subplots(nrows=1,
                               ncols=1,
                               figsize=figsize,
                               gridspec_kw={"width_ratios": [figsize[0]],
                                            "height_ratios": [figsize[1]]})
        
        # Add title
        if title is not None:
            if watermark:
                fig.suptitle(title + "\n[made with ezGPX]", fontsize=title_fontsize)
            else:
                fig.suptitle(title, fontsize=title_fontsize)

        # Set figure layout
        fig.tight_layout()

        # Set axes aspect ratio
        ax.set_aspect(figsize[1] / figsize[0], adjustable="datalim")
        pos = ax.get_position() # Axes bounding box
        print(f"pos.width = {pos.width}")
        print(f"pos.height = {pos.height}")

        # Plot map
        # Does not work...
        self.expert_map(axes=ax,
                        size=size,
                        color=color,
                        cmap=cmap,
                        colorbar=colorbar,
                        start_point_color=start_point_color,
                        stop_point_color=stop_point_color,
                        way_points_color=way_points_color,
                        background=background,
                        offset_percentage=offset_percentage,
                        xpixels=None,
                        ypixels=None,
                        dpi=dpi)

        # Save or display plot
        if file_path is not None:
            # Check if provided path exists
            directory_path = os.path.dirname(os.path.realpath(file_path))
            if not os.path.exists(directory_path):
                logging.error("Provided path does not exist")
                return
            plt.savefig(file_path)
        else:
            plt.show()

        return fig, ax
    
    def matplotlib_plot(
            self,
            figsize: Tuple[int, int] = (16, 9),
            size: float = 10,
            color: str = "#101010",
            cmap: Optional[mpl.colors.Colormap] = None,
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
            file_path: str = None):
        # Create dataframe containing data from the GPX file
        self.dataframe = self.to_dataframe(elevation=True,
                                           time=True,
                                           speed=True,
                                           pace=True,
                                           ascent_rate=True,
                                           ascent_speed=True,
                                           distance_from_start=True)
        
        # Create figure
        fig = plt.figure(figsize=figsize)
        
        # Compute track boundaries
        min_lat, min_lon, max_lat, max_lon = self.bounds()

        # Add default offset
        delta_max = max(max_lat - min_lat, max_lon - min_lon)
        offset = delta_max * offset_percentage
        min_lat, min_lon = max(0, min_lat - offset), max(0, min_lon - offset)
        max_lat, max_lon = min(max_lat + offset, 90),  min(max_lon + offset, 180)
        
        # Some sort of magic to achieve the correct map aspect ratio
        # CREATE FUNCTION (also used in anmation??)
        lat_offset = 1e-5
        lon_offset = 1e-5
        delta_lat = max_lat - min_lat
        delta_lon = max_lon - min_lon
        r = delta_lon / delta_lat # Current map aspect ratio
        r_ref = figsize[0] / figsize[1] # Target map aspect ratio, Adapt in function of the shape of the subplot...

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
        map = Basemap(projection="cyl",
                      llcrnrlon=min_lon,
                      llcrnrlat=min_lat,
                      urcrnrlon=max_lon,
                      urcrnrlat=max_lat)
        
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
            map.arcgisimage(service=background,
                            dpi=dpi,
                            verbose=True)
            
        # Scatter track points
        x, y = map(self.dataframe["lon"], self.dataframe["lat"]) # Project track points
        x, y = x.tolist(), y.tolist()                            # Convert to list
        if color in ["ele", "speed", "pace", "vertical_drop", "ascent_rate", "ascent_speed"]:
            im = map.scatter(self.dataframe["lon"],
                             self.dataframe["lat"],
                             s=size,
                             c=self.dataframe[color],
                             cmap=cmap)
        else:
            im = map.scatter(self.dataframe["lon"],
                             self.dataframe["lat"],
                             s=size,
                             color=color)
            
        # Scatter start point with different color
        if start_point_color:
            map.scatter(x[0], y[0], marker="^",
                        color=start_point_color)

        # Scatter stop point with different color
        if stop_point_color:
            map.scatter(x[-1], y[-1], marker="h",
                        color=stop_point_color)

        # Scatter way points with different color
        if way_points_color:
            for way_point in self.gpx.wpt:
                x, y = map(way_point.lon, way_point.lat) # Project way point
                map.scatter(x, y, marker="D",
                            color=way_points_color)      # Scatter way point
            
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

        # Save or display plot
        if file_path is not None:
            # Check if provided path exists
            directory_path = os.path.dirname(os.path.realpath(file_path))
            if not os.path.exists(directory_path):
                logging.error("Provided path does not exist")
                return
            fig.savefig(file_path)
        else:
            fig.show()

        return fig

###############################################################################
#### Expert Plot ##############################################################
###############################################################################
    
    def check_axes_position(
            self,
            subplots: Tuple[int, int],
            position: Tuple[int, int]):
        """
        Check position existence in the array of subplots.

        Parameters
        ----------
        subplots : Tuple[int, int]
            Number of rows and columns of subplots in the figure
        position : Tuple[int, int]
            Potential position of a subplot in the figure 

        Returns
        -------
        bool
            True if the subplot position exists in the figure
        """
        # Retrieve data
        nb_rows, nb_columns = subplots
        row, column = position

        # Check row index
        if row < 0 or row >= nb_rows:
            return False
        
        # Check column index
        if column < 0 or column >= nb_columns:
            return False
        
        # Valid position
        return True

    def expert_map(
            self,
            axes: Axes,
            size: float = 10,
            color: str = "#101010",
            cmap: Optional[mpl.colors.Colormap] = None,
            colorbar: bool = False,
            start_point_color: Optional[str] = None,
            stop_point_color: Optional[str] = None,
            way_points_color: Optional[str] = None,
            background: Optional[str] = None,
            offset_percentage: float = 0.04,
            xpixels: int = 400,
            ypixels: Optional[int] = None,
            dpi: int = 96):
        # Clear axes
        axes.clear()
        
        # Compute track boundaries
        min_lat, min_lon, max_lat, max_lon = self.bounds()

        # Add default offset
        delta_max = max(max_lat - min_lat, max_lon - min_lon)
        offset = delta_max * offset_percentage
        min_lat, min_lon = max(0, min_lat - offset), max(0, min_lon - offset)
        max_lat, max_lon = min(max_lat + offset, 90), min(max_lon + offset, 180)

        # Some sort of magic to achieve the correct map aspect ratio
        # CREATE FUNCTION (also used in anmation??)
        lat_offset = 1e-5
        lon_offset = 1e-5
        delta_lat = max_lat - min_lat
        delta_lon = max_lon - min_lon
        r = delta_lon / delta_lat # Current map aspect ratio
        pos = axes.get_position() # Axes bounding box
        print(f"pos.width = {pos.width}")
        print(f"pos.height = {pos.height}")
        r_ref = pos.width / pos.height # Target map aspect ratio, Adapt in function of the shape of the subplot...

        tolerance = 1e-3
        # while (not isclose(r, r_ref, abs_tol=tolerance) or 
        #        not isclose(delta_lon % pos.width, 0.0, abs_tol=tolerance) or
        #        not isclose(delta_lat % pos.height, 0.0, abs_tol=tolerance)):
        # while not isclose(r, r_ref, abs_tol=tolerance):
        #     if r > r_ref:
        #         min_lat = max(0, min_lat - lat_offset)
        #         max_lat = min(max_lat + lat_offset, 90)
        #         delta_lat = max_lat - min_lat
        #     if r < r_ref:
        #         min_lon = max(0, min_lon - lon_offset)
        #         max_lon = min(max_lon + lon_offset, 180)
        #         delta_lon = max_lon - min_lon
        #     r = delta_lon / delta_lat

        # print(f"delta_lon = {delta_lon}")
        # print(f"delta_lat = {delta_lat}")
        # print(f"r_ref = {r_ref}")
        # print(f"r = {r}")
        # print(f"delta_lon % pos.width = {delta_lon % pos.width}")
        # print(f"delta_lat % pos.height = {delta_lat % pos.height}")

        # Create map
        map = Basemap(projection="cyl",
                      llcrnrlon=min_lon,
                      llcrnrlat=min_lat,
                      urcrnrlon=max_lon,
                      urcrnrlat=max_lat,
                      ax=axes)
        
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
            map.arcgisimage(service=background,
                            # xpixels=xpixels,
                            # ypixels=ypixels,
                            dpi=dpi,
                            verbose=True)
            
        # Scatter track points
        x, y = map(self.dataframe["lon"], self.dataframe["lat"]) # Project track points
        x, y = x.tolist(), y.tolist()                            # Convert to list
        if color in ["ele", "speed", "pace", "vertical_drop", "ascent_rate", "ascent_speed"]:
            im = map.scatter(self.dataframe["lon"],
                             self.dataframe["lat"],
                             s=size,
                             c=self.dataframe[color],
                             cmap=cmap)
        else:
            im = map.scatter(self.dataframe["lon"],
                             self.dataframe["lat"],
                             s=size,
                             color=color)
            
        # Scatter start point with different color
        if start_point_color:
            map.scatter(x[0], y[0], marker="^",
                        color=start_point_color)

        # Scatter stop point with different color
        if stop_point_color:
            map.scatter(x[-1], y[-1], marker="h",
                        color=stop_point_color)

        # Scatter way points with different color
        if way_points_color:
            for way_point in self.gpx.wpt:
                x, y = map(way_point.lon, way_point.lat) # Project way point
                map.scatter(x, y, marker="D",
                            color=way_points_color)      # Scatter way point
            
        # Colorbar
        if colorbar:
            plt.colorbar(im,
                         ax=axes)

        return im

    def expert_elevation_profile(
            self,
            axes: Axes,
            x_type: str,
            size: float = 10,
            color: str = "#101010",
            cmap: Optional[mpl.colors.Colormap] = None,
            colorbar: bool = False,
            grid: bool = False,
            fill_color: Optional[str] = None,
            fill_alpha: float = 0.5):
        # Clear axes
        axes.clear()

        # Compute x values
        x = None
        x_label = ""
        if x_type == "distance":
            x = self.dataframe["distance_from_start"] / 1000 # Convert to km
            x_label = "Distance [km]"
        elif x_type == "time":
            x = self.dataframe["time"]
            # x = [t.to_pydatetime().time() for t in tmp_x]
            # x = [t.to_pydatetime() for t in tmp_x]
            x_label = "Time"
        else:
            logging.error(f"Invalid x_type argument {x_type}")
            return

        # Plot
        if color in ["ele", "speed", "pace", "vertical_drop", "ascent_rate", "ascent_speed"]:
            im = axes.scatter(x,
                              self.dataframe["ele"],
                              s=size,
                              c=self.dataframe[color],
                              cmap=cmap)
        else:
            im = axes.scatter(x,
                              self.dataframe["ele"],
                              s=size,
                              color=color)

        # Grid
        if grid:
            axes.grid()

        # Fill
        if fill_color:
            axes.fill_between(x,
                              [0 for i in range(len(x))],
                              self.dataframe["ele"],
                              color=fill_color,
                              alpha=fill_alpha)
              
        # Colorbar
        if colorbar:
            plt.colorbar(im,
                         ax=axes)

        # Axis labels
        axes.set_xlabel(x_label)
        axes.set_ylabel("Elevation [m]")

        # Axis ticks
        # WTF ???
        # if x_type == "time":
        #     x_ticks = axes.get_xticks()
        #     print(x_ticks)
        #     print(type(x_ticks[0]))
        #     axes.set_xticks(x_ticks)

    def expert_pace_graph(
            self,
            axes: Axes,
            x_type: str,
            size: float = 10,
            color: str = "#101010",
            cmap: Optional[mpl.colors.Colormap] = None,
            colorbar: bool = False,
            grid: bool = False,
            fill_color: Optional[str] = None,
            fill_alpha: float = 0.5,
            threshold: float = 60.0):
        # Clear axes
        axes.clear()

        # Compute x values
        x = None
        x_label = ""
        if x_type == "distance":
            x = self.dataframe["distance_from_start"].values / 1000 # Convert to km
            x_label = "Distance [km]"
        elif x_type == "time":
            x = self.dataframe["time"].values
            x_label = "Time"
        else:
            logging.error(f"Invalid x_type argument {x_type}")
            return

        # Plot
        if color in ["ele", "speed", "pace", "vertical_drop", "ascent_rate", "ascent_speed"]:
            # Remove lowest values
            pace = self.dataframe["pace"].values
            color = self.dataframe[color]
            tmp = [(x, p, c) for (x, p, c) in list(zip(x, pace, color)) if p < threshold]
            x = [x for (x, p, c) in tmp]
            pace = [p for (x, p, c) in tmp]
            color = [c for (x, p, c) in tmp]
            im = axes.scatter(x,
                              pace,
                              s=size,
                              c=color,
                              cmap=cmap) # .values to avoid -> Multi-dimensional indexing (e.g. `obj[:, None]`) is no longer supported. Convert to a numpy array before indexing instead.
        else:
            # Remove lowest values
            pace = self.dataframe["pace"].values
            tmp = [(x, p) for (x,p) in list(zip(x, pace)) if p < threshold]
            x = [x for (x,p) in tmp]
            pace = [p for (x,p) in tmp]
            im = axes.scatter(x,
                              pace,
                              s=size,
                              color=color) # .values to avoid -> Multi-dimensional indexing (e.g. `obj[:, None]`)
        axes.invert_yaxis()

        # Grid
        if grid:
            axes.grid()

        # Fill
        if fill_color:
            max_pace = max(pace)
            axes.fill_between(x,
                              [max_pace for i in range(len(x))],
                              pace,
                              color=fill_color,
                              alpha=fill_alpha)

        # Colorbar
        if colorbar:
            plt.colorbar(im,
                         ax=axes)

        # Axis labels
        axes.set_xlabel(x_label)
        axes.set_ylabel("Pace [min/km]")

    def expert_ascent_rate_graph(
            self,
            axes: Axes):
        # Clear axes
        axes.clear()

        ascent_rates = [None, 2, 4, 6, 8, 10, 12, 14, 16, 18]
        nb_ascent_rates = [0 for i in ascent_rates]
        nb_points = 0

        # Compute number of points for each ascent rate zone
        for track in self.gpx.tracks:
            for track_segment in track.trkseg:
                nb_points += len(track_segment.trkpt)
                for track_point in track_segment.trkpt:
                    i = len(ascent_rates) - 1
                    while i > 0 and abs(track_point.ascent_rate) < ascent_rates[i]:
                        i -= 1
                    nb_ascent_rates[i] += 1

        # Compute percentage for each ascent rate zone
        percent_ascent_rate = [(nb * 100) / nb_points for nb in nb_ascent_rates]

        # Create position and labels
        y_pos = range(1, len(ascent_rates)+1)
        y_labels = [f"{x} %" if x is not None else "" for x in ascent_rates]

        # Plot horizontal bar graph
        rects = axes.barh(y=y_pos,
                          width=percent_ascent_rate,
                          color=["lightgray", "lightgreen",
                                 "limegreen", "green",
                                 "yellow", "gold",
                                 "orange", "red",
                                 "purple", "black"])
        
        # Add legend on bars (percentiles)
        largest_percentile = max(percent_ascent_rate)
        large_percentiles = [f"{p:.1f} %" if abs(p - largest_percentile) < 10 else "" for p in percent_ascent_rate]
        small_percentiles = [f"{p:.1f} %" if abs(p - largest_percentile) >= 10 else "" for p in percent_ascent_rate]
        axes.bar_label(rects, small_percentiles,
                       padding=5, color="black", fontweight="bold")
        axes.bar_label(rects, large_percentiles,
                       padding=-40, color="white", fontweight="bold")
        
        # Set y-ticks with labels
        axes.set_yticks(y_pos, labels=y_labels)

        # Add title
        axes.set_title("Ascent rate")

    def expert_data_table(
            self,
            axes: Axes):
        # Clear axes
        axes.clear()
        
        # Compute table bounding box
        pos = axes.get_position()
        bbox = [pos.x0, pos.y0, pos.width, pos.height] # No change

        # Row labels
        row_labels = [
            "Distance",
            "Total ascent",
            "Total descent",
            "Total time",
            "Avg. speed",
            "Avg. moving speed",
            "Maximum speed",
            "Moving time"
        ]

        # Data
        data = [
            [f"{self.distance()/1000:.2f} km"],
            [f"{self.ascent():.2f} m"],
            [f"{self.descent():.2f} m"],
            [f"{self.total_elapsed_time()}"],
            [f"{self.avg_speed():.2f} km/h"],
            [f"{self.avg_moving_speed():.2f} km/h"],
            [f"{self.max_speed():.2f} km/h"],
            [f"{self.moving_time()}"]
        ]

        # Create table
        table = axes.table(cellText=data,
                           rowLabels=row_labels,
                           bbox=bbox,
                           loc="right",
                           edges="open")

        # Remove axis
        axes.axis("off")

    def expert_image(
            self,
            axes: Axes,
            img_path: str,
            img_legend: str):
        # Clear axes
        axes.clear()
        
        # Plot image
        img = plt.imread(img_path)
        axes.imshow(img)

        # Add title
        axes.set_title(img_legend)

        # Remove axes ticks
        axes.set_xticks([])
        axes.set_yticks([])

    def expert_made_with_ezgpx(
            self,
            axes: Axes):
        # Clear axes
        axes.clear()

        # Plot text
        text_kwargs = dict(ha="center",
                           va="center",
                           fontsize=26,
                           color="black",
                           rotation=0,
                           bbox=dict(boxstyle="square",
                                     ec="black",
                                     fc="lightgray"))
        axes.text(0.5 , 0.5, "Made with ezGPX", **text_kwargs)

        # Remove axes
        axes.axis("off")

    def expert_plot(
            self,
            figsize: Tuple[int, int] = (16,9),
            subplots: Tuple[int, int] = (1,1),
            width_ratios: List = None,
            height_ratios: List = None,
            map_position: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]] = (0,0),
            map_size: float = 10,
            map_color: str = "#101010",
            map_cmap: Optional[mpl.colors.Colormap] = None,
            map_colorbar: bool = False,
            start_point_color: Optional[str] = None,
            stop_point_color: Optional[str] = None,
            way_points_color: Optional[str] = None,
            background: Optional[str] = "World_Imagery",
            offset_percentage: float = 0.04,
            xpixels: int = 400,
            ypixels: Optional[int] = None,
            dpi: int = 96,
            elevation_profile_position: Optional[Tuple[int, int]] = (1,0), # None
            elevation_profile_x_type: Optional[str] = None, # "distance", "time"
            elevation_profile_size: float = 10,
            elevation_profile_color: str = "#101010",
            elevation_profile_cmap: Optional[mpl.colors.Colormap] = None,
            elevation_profile_colorbar: bool = False,
            elevation_profile_grid: bool = False,
            elevation_profile_fill_color: Optional[str] = None,
            elevation_profile_fill_alpha: float = 0.5,
            pace_graph_position: Optional[Tuple[int, int]] = (2,0), # None
            pace_graph_x_type: Optional[str] = None, # "distance", "time"
            pace_graph_size: float = 10,
            pace_graph_color: str = "#101010",
            pace_graph_cmap: Optional[mpl.colors.Colormap] = None,
            pace_graph_colorbar: bool = False,
            pace_graph_grid: bool = False,
            pace_graph_fill_color: Optional[str] = None,
            pace_graph_fill_alpha: float = 0.5,
            pace_graph_threshold: float = 60.0,
            ascent_rate_graph_position: Optional[Tuple[int, int]] = (0,1), # None
            data_table_position: Optional[Tuple[int, int]] = (1,1), # None
            img_position: Optional[Tuple[int, int]] = None,
            img_path: Optional[str] = None,
            img_legend: Optional[str] = None,
            made_with_ezgpx_position: Optional[Tuple[int, int]] = (0,1), # None
            shared_color: str = "#101010",
            shared_cmap: Optional[mpl.colors.Colormap] = None,
            shared_colorbar: bool = False,
            title: Optional[str] = None,
            title_fontsize: int = 20,
            watermark: bool = False,
            file_path: Optional[str] = None):
        # Create dataframe containing data from the GPX file
        self.dataframe = self.to_dataframe(elevation=True,
                                           time=True,
                                           speed=True,
                                           pace=True,
                                           ascent_rate=True,
                                           ascent_speed=True,
                                           distance_from_start=True)
        
        # Create figure with axes
        fig, axs = plt.subplots(nrows=subplots[0],
                                ncols=subplots[1],
                                figsize=figsize,
                                layout="constrained",
                                gridspec_kw={"width_ratios": width_ratios,
                                             "height_ratios": height_ratios})
        
        # Reshape axs for single line/column plots
        if subplots[0] == 1 or subplots[1] == 1:
            axs = axs.reshape((subplots[0], subplots[1]))
        
        # Add title
        if title is not None:
            if watermark:
                fig.suptitle(title + "\n[made with ezGPX]", fontsize=title_fontsize)
            else:
                fig.suptitle(title, fontsize=title_fontsize)

        # Initialize im
        im = None

        # Handle map plot
        map_ax = None
        if map_position is not None:
            if isinstance(map_position, tuple):
                # Check if map_position is correct
                if not self.check_axes_position(subplots, map_position):
                    logging.error(f"Invalid map_position argument: no subplot {map_position} in a {subplots} array of plots")
                    return
                
                # Retrieve map axis
                map_ax = axs[map_position]

                # Set axes aspect ratio
                width_ratio = 1
                height_ratio = 1
                if width_ratios is not None:
                    width_ratio = width_ratios[map_position[0]]
                if height_ratios is not None:
                    height_ratio = height_ratios[map_position[1]]
                map_ax.set_aspect(width_ratio / height_ratio, adjustable="datalim")                
            else:
                # Check if map_position is correct
                for map_p in map_position:
                    if not self.check_axes_position(subplots, map_p):
                        logging.error(f"Invalid map_position argument: no subplot {map_position} in a {subplots} array of plots")
                        return
                    
                gridspec = axs[0, 0].get_subplotspec().get_gridspec()

                # Remove unused subplots and retrieve subfigure span
                # USE LAMBDA OR SOMETHING CLEANER
                min_row = map_position[0][0]
                max_row = map_position[0][0]
                min_col = map_position[0][1]
                max_col = map_position[0][1]
                for map_p in map_position:
                    axs[map_p].remove()
                    if map_p[0] < min_row:
                        min_row = map_p[0]
                    if map_p[0] > max_row:
                        max_row = map_p[0]
                    if map_p[1] < min_col:
                        min_col = map_p[1]
                    if map_p[1] > max_col:
                        max_col = map_p[1]

                subfig = fig.add_subfigure(gridspec[min_row:max_row+1, min_col:max_col+1])
                # subfig.set_facecolor("0.75") # For testing purpose
                map_ax = subfig.subplots(nrows=1, ncols=1)

            # Plot map on subplot
            im = self.expert_map(map_ax,
                                 size=map_size,
                                 color=map_color,
                                 cmap=map_cmap,
                                 colorbar=map_colorbar if not shared_colorbar else False,
                                 start_point_color=start_point_color,
                                 stop_point_color=stop_point_color,
                                 way_points_color=way_points_color,
                                 background=background,
                                 offset_percentage=offset_percentage,
                                 xpixels=xpixels,
                                 ypixels=ypixels,
                                 dpi=dpi)
            
        # Handle elevation profile plot
        if elevation_profile_position is not None:
            # Check if elevation_profile_position is correct
            if self.check_axes_position(subplots, elevation_profile_position):
                # Plot elevation profile on subplot
                self.expert_elevation_profile(axs[elevation_profile_position],
                                              x_type=elevation_profile_x_type,
                                              size=elevation_profile_size,
                                              color=elevation_profile_color,
                                              cmap=elevation_profile_cmap,
                                              colorbar=elevation_profile_colorbar,
                                              grid=elevation_profile_grid,
                                              fill_color=elevation_profile_fill_color,
                                              fill_alpha=elevation_profile_fill_alpha)
            else:
                logging.error(f"Invalid elevation_profile_position argument: no subplot {elevation_profile_position} in a {subplots} array of plots")
                return
            
        # Handle pace graph plot
        if pace_graph_position is not None:
            # Check if pace_graph_position is correct
            if self.check_axes_position(subplots, pace_graph_position):
                # Plot pace on subplot
                self.expert_pace_graph(axs[pace_graph_position],
                                       x_type=pace_graph_x_type,
                                       size=pace_graph_size,
                                       color=pace_graph_color,
                                       cmap=pace_graph_cmap,
                                       colorbar=pace_graph_colorbar,
                                       grid=pace_graph_grid,
                                       fill_color=pace_graph_fill_color,
                                       fill_alpha=pace_graph_fill_alpha,
                                       threshold=pace_graph_threshold)
            else:
                logging.error(f"Invalid pace_graph_position argument: no subplot {pace_graph_position} in a {subplots} array of plots")
                return
            
        # Handle ascent rate bar graph
        if ascent_rate_graph_position is not None:
            # Check if ascent_rate_graph_position is correct
            if self.check_axes_position(subplots, ascent_rate_graph_position):
                # Plot bar graph on subplot
                self.expert_ascent_rate_graph(axs[ascent_rate_graph_position[0], ascent_rate_graph_position[1]])
            else:
                logging.error(f"Invalid ascent_rate_graph_position position: no subplot {ascent_rate_graph_position} in a {subplots} array of plots")
                return
            
        # Handle data table plot
        if data_table_position is not None:
            # Check if data_table_position is correct
            if self.check_axes_position(subplots, data_table_position):
                gridspec = axs[0, 0].get_subplotspec().get_gridspec()
                axs[data_table_position].remove()
                subfig_ = fig.add_subfigure(gridspec[data_table_position])
                data_ax = subfig_.subplots(nrows=1, ncols=1)
                # Plot data table on subplot
                self.expert_data_table(data_ax)
            else:
                logging.error(f"Invalid data_table_position argument: no subplot {data_table_position} in a {subplots} array of plots")
                return
            
        # Handle image
        if img_position is not None:
            # Check if img_position is correct
            if self.check_axes_position(subplots, img_position):
                # Plot image on subplot
                self.expert_image(axs[img_position],
                                  img_path,
                                  img_legend)
            else:
                logging.error(f"Invalid img_position argument: no subplot {img_position} in a {subplots} array of plots")
                return

        # Handle ascent rate bar graph
        if made_with_ezgpx_position is not None:
            # Check if made_with_ezgpx_position is correct
            if self.check_axes_position(subplots, made_with_ezgpx_position):
                # Plot text on subplot
                self.expert_made_with_ezgpx(axs[made_with_ezgpx_position])
            else:
                logging.error(f"Invalid made_with_ezgpx_position argument: no subplot {made_with_ezgpx_position} in a {subplots} array of plots")
                return
            
        if shared_color and im:
            if shared_cmap is None:
                shared_cmap = mpl.cm.get_cmap("viridis", 12)


            cb_ax = fig.add_axes([1.025, 0, 0.02, 1])
            cbar = fig.colorbar(im, cax=cb_ax)
            # fig.colorbar(im,
            #              ax=axs.ravel().tolist())
            
        # Save or display plot
        if file_path is not None:
            # Check if provided path exists
            directory_path = os.path.dirname(os.path.realpath(file_path))
            if not os.path.exists(directory_path):
                logging.error("Provided path does not exist")
                return
            plt.savefig(file_path)
        else:
            plt.show()

###############################################################################
#### Google Maps Plot #########################################################
###############################################################################

    def gmplot_plot(
            self,
            color: str = "#110000",
            start_stop_colors: Optional[Tuple[str, str]] = None,
            way_points_color: Optional[str] = None,
            zoom: float = 10.0,
            title: Optional[str] = None,
            file_path: str = None,
            open: bool = True,
            scatter: bool = False,
            plot: bool = True):
        """
        Plot GPX using gmplot.

        Parameters
        ----------
        color : str, optional
            Track color, by default "#110000"
        start_stop_colors : Optional[Tuple[str, str]], optional
            Start and stop points colors, by default None
        way_points_color : Optional[str], optional
            Way points color, by default None
        zoom : float, optional
            Zoom, by default 10.0
        title : Optional[str], optional
            Title, by default None
        file_path : str, optional
            Path to save plot, by default None
        open : bool, optional
            Open the plot in the default web browser, by default True
        scatter : bool, optional
            Scatter track points, by default False
        plot : bool, optional
            Plot track points, by default True
        """
        # Create plotter
        center_lat, center_lon = self.center()
        map = gmplot.GoogleMapPlotter(center_lat, center_lon, zoom)

        # Create dataframe containing data from the GPX file
        gpx_df = self.to_dataframe()

        # Scatter track points
        if scatter:
            map.scatter(gpx_df["lat"], gpx_df["lon"],
                        color, size=5, marker=False)
        if plot:
            map.plot(gpx_df["lat"], gpx_df["lon"],
                     color, edge_width=2.5)
        
        # Scatter start and stop points with different color
        if start_stop_colors:
            map.scatter([self.gpx.tracks[0].trkseg[0].trkpt[0].lat],
                        [self.gpx.tracks[0].trkseg[0].trkpt[0].lon],
                        start_stop_colors[0], size=5, marker=True)
            map.scatter([self.gpx.tracks[-1].trkseg[-1].trkpt[-1].lat],
                        [self.gpx.tracks[-1].trkseg[-1].trkpt[-1].lon],
                        start_stop_colors[1], size=5, marker=True)
            
        # Scatter way points with different color
        if way_points_color:
            for way_point in self.gpx.wpt:
                map.scatter([way_point.lat], [way_point.lon],
                            way_points_color, size=5, marker=True)
        
        # Add title
        if title is not None:
            map.text(center_lat, center_lon, self.name(), color="#FFFFFF")

        # Save map
        map.draw(file_path)

        # Open map in web browser
        if open:
            webbrowser.open(file_path)

###############################################################################
#### Folium Plot ##############################################################
###############################################################################

    def folium_plot(
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
            open: bool = True):
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
        open : bool, optional
            Open the plot in the default web browser, by default True
        """
        # Create map
        center_lat, center_lon = self.center()
        m = folium.Map(location=[center_lat, center_lon],
                       zoom_start=zoom,
                       tiles=tiles)
        
        # Plot track points
        gpx_df = self.to_dataframe()
        gpx_df["coordinates"] = list(
            zip(gpx_df.lat, gpx_df.lon))
        folium.PolyLine(gpx_df["coordinates"],
                        tooltip=self.name(), color=color).add_to(m)

        # Scatter start and stop points with different color
        if start_stop_colors:
            folium.Marker([self.gpx.tracks[0].trkseg[0].trkpt[0].lat, self.gpx.tracks[0].trkseg[0].trkpt[0].lon],
                          popup="<b>Start</b>", tooltip="Start", icon=folium.Icon(color=start_stop_colors[0])).add_to(m)
            folium.Marker([self.gpx.tracks[-1].trkseg[-1].trkpt[-1].lat, self.gpx.tracks[-1].trkseg[-1].trkpt[-1].lon],
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
            file_path = self.file_path[:-4] + ".html"
        m.save(file_path)

        # Open map in web browser
        if open:
            webbrowser.open(file_path)

###############################################################################
#### PaperMap Plot ############################################################
###############################################################################
            
    def papermap_plot(
            self,
            lat: Optional[float] = None,
            lon: Optional[float] = None,
            tile_server: str = "OpenStreetMap",
            api_key: Optional[str] = None,
            size: str = "a4",
            use_landscape: bool = True,
            margin_top: int = 10,
            margin_right: int = 10,
            margin_bottom: int = 10,
            margin_left: int = 10,
            scale: int = 25000,
            dpi: int = 300,
            background_color: str = "#FFF",
            add_grid: bool = False,
            grid_size: int = 1000,
            file_path: Optional[str] = None):
        """
        Create background map of the GPX using PaperMap.

        Parameters
        ----------
        lat : Optional[float], optional
            Latitude of the center of the map, by default None
        lon : Optional[float], optional
            Longitude of the center of the map, by default None
        tile_server : str, optional
            Tile server to serve as the base of the paper map, by default "OpenStreetMap"
        api_key : Optional[str], optional
            API key for the chosen tile server (if applicable), by default None
        size : str, optional
            Size of the paper map, by default "a4"
        use_landscape : bool, optional
            Use landscape orientation, by default True
        margin_top : int, optional
            Top margin (in mm), by default 10
        margin_right : int, optional
            Right margin (in mm), by default 10
        margin_bottom : int, optional
            Bottom margin (in mm), by default 10
        margin_left : int, optional
            Left margin (in mm), by default 10
        scale : int, optional
            Scale of the paper map, by default 25000
        dpi : int, optional
            Dots per inch, by default 300
        background_color : str, optional
            Background color of the paper map, by default "#FFF"
        add_grid : bool, optional
            Add a coordinate grid overlay to the paper map, by default False
        grid_size : int, optional
            Size of the grid squares (if applicable, in meters), by default 1000
        file_path : Optional[str], optional
            Path to save plot, by default None
        """
        # Create map
        center_lat, center_lon = self.center()
        if lat is None:
            lat = center_lat
        if lon is None:
            lon = center_lon
        
        pm = PaperMap(lat=lat,
                      lon=lon,
                      tile_server=tile_server,
                      api_key=api_key,
                      size=size,
                      use_landscape=use_landscape,
                      margin_top=margin_top,
                      margin_right=margin_right,
                      margin_bottom=margin_bottom,
                      margin_left=margin_left,
                      scale=scale,
                      dpi=dpi,
                      background_color=background_color,
                      add_grid=add_grid,
                      grid_size=grid_size)
        
        # Render map
        pm.render()

        # Save map
        if file_path is None:
            file_path = self.file_path[:-4] + ".pdf"
        pm.save(file_path)

###############################################################################
#### Animated Plot #########################################################
###############################################################################


    def _broken_matplotlib_animation_(
            self,
            figsize: Tuple[int, int] = (16, 9),
            size: float = 10,
            color: str = "#101010",
            cmap: Optional[mpl.colors.Colormap] = None,
            colorbar: bool = False,
            start_point_color: Optional[str] = None,
            stop_point_color: Optional[str] = None,
            way_points_color: Optional[str] = None,
            background: Optional[str] = None,
            offset_percentage: float = 0.04,
            dpi: int = 96,
            interval: float = 20,
            fps: int = 24,
            repeat: bool = True,
            title: Optional[str] = None,
            title_fontsize: int = 20,
            watermark: bool = False,
            file_path: str = None):
        # Create dataframe containing data from the GPX file
        self.dataframe = self.to_dataframe(elevation=True,
                                           speed=True,
                                           pace=True,
                                           ascent_rate=True,
                                           ascent_speed=True,
                                           distance_from_start=True)
        
        # Retrieve useful data
        lat = self.dataframe["lat"].values
        lon = self.dataframe["lon"].values
        min_lat, min_lon, max_lat, max_lon = self.bounds()

        # Create figure with axes
        fig, ax = plt.subplots(nrows=1,
                                ncols=1,
                                figsize=figsize,
                                gridspec_kw={"width_ratios": [figsize[0]],
                                            "height_ratios": [figsize[1]]})
        
        # Add title
        if title is not None:
            if watermark:
                fig.suptitle(title + "\n[made with ezGPX]", fontsize=title_fontsize)
            else:
                fig.suptitle(title, fontsize=title_fontsize)

        # Set figure layout
        fig.tight_layout()

        # Set axes aspect ratio
        ax.set_aspect(figsize[1] / figsize[0], adjustable="datalim")
        # pos = ax.get_position() # Axes bounding box
        # print(f"pos = {pos.width}")
        # print(f"pos = {pos.height}")

        # Create map
        # ADD CHOICE !!!
        map = Basemap(projection="cyl",
                      llcrnrlon=min_lon,
                      llcrnrlat=min_lat,
                      urcrnrlon=max_lon,
                      urcrnrlat=max_lat,
                      ax=ax)
        map.arcgisimage(service=background,
                        dpi=dpi,
                        verbose=True)
        
        # Create empty line
        # Add marker, marker style...
        line, = ax.plot([], [], color=color, linewidth=size)

        # Animation function
        def animate(i):
            # Clear line at the beginning of the animation
            if i == 0:
                line.set_xdata([])
                line.set_ydata([])

            try:
                line.set_xdata(np.concatenate((line.get_xdata(), np.array([lon[i]]))))
                line.set_ydata(np.concatenate((line.get_ydata(), np.array([lat[i]]))))
            except:
                print("No more data point, you need to stop!!")

            return line,

        # Create animation
        ani = animation.FuncAnimation(fig=fig,
                                      func=animate,
                                      frames=len(lat),
                                      interval=interval, # Delay between frames in ms
                                      repeat=True if file_path is None else repeat) # ?

        # Save or display plot
        if file_path is not None:
            # Check if provided path exists
            directory_path = os.path.dirname(os.path.realpath(file_path))
            if not os.path.exists(directory_path):
                logging.error("Provided path does not exist")
                return
            ani.save(file_path, fps=fps, dpi=dpi)
        else:
            ani.show()

        return fig, ax
    
    def matplotlib_animation(
            self,
            figsize: Tuple[int, int] = (16, 9),
            size: float = 10,
            color: str = "#101010",
            cmap: Optional[mpl.colors.Colormap] = None,
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
        Crashes may be due to parameters exceeding system capabilities.
        Try reducing fps and/or bitrate.
        """
        # Create dataframe containing data from the GPX file
        self.dataframe = self.to_dataframe()
        
        # Retrieve useful data
        lat = self.dataframe["lat"].values
        lon = self.dataframe["lon"].values
        
        # Create figure
        fig = plt.figure(figsize=figsize)
        
        # Compute track boundaries
        min_lat, min_lon, max_lat, max_lon = self.bounds()

        # Add default offset
        delta_max = max(max_lat - min_lat, max_lon - min_lon)
        offset = delta_max * offset_percentage
        min_lat, min_lon = max(0, min_lat - offset), max(0, min_lon - offset)
        max_lat, max_lon = min(max_lat + offset, 90),  min(max_lon + offset, 180)
        
        # Some sort of magic to achieve the correct map aspect ratio
        # CREATE FUNCTION (also used in anmation??)
        lat_offset = 1e-5
        lon_offset = 1e-5
        delta_lat = max_lat - min_lat
        delta_lon = max_lon - min_lon
        r = delta_lon / delta_lat # Current map aspect ratio
        r_ref = figsize[0] / figsize[1] # Target map aspect ratio, Adapt in function of the shape of the subplot...

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
        map = Basemap(projection="cyl",
                      llcrnrlon=min_lon,
                      llcrnrlat=min_lat,
                      urcrnrlon=max_lon,
                      urcrnrlat=max_lat)
        
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
            map.arcgisimage(service=background,
                            dpi=dpi,
                            verbose=True)
            
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
                line.set_xdata(np.concatenate((line.get_xdata(), np.array([lon[i]]))))
                line.set_ydata(np.concatenate((line.get_ydata(), np.array([lat[i]]))))
            except:
                print("No more data point, you need to stop!!")

            return line,

        # Create animation
        ani = animation.FuncAnimation(fig=fig,
                                      func=animate,
                                      frames=len(lat),
                                      interval=interval, # Delay between frames in ms
                                      repeat=repeat if file_path is None else False) # ?
            
        # Colorbar
        # if colorbar:
        #     fig.colorbar(im)

        # Add title
        if title is not None:
            if watermark:
                fig.suptitle(title + "\n[made with ezGPX]", fontsize=title_fontsize)
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
            ani.show()

        return fig