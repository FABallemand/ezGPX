import logging
from typing import *

import xml.etree.ElementTree as ET

from ..gpx_elements import GPX, Metadata, Track, TrackSegment, TrackPoint

class Parser():

    def __init__(self, gpx_file: str = ""):
        self.gpx_file = gpx_file
        self.gpx_tree = None
        self.gpx_root = None
        self.name_space = {"topo": "http://www.topografix.com/GPX/1/1"}
        self.gpx = GPX()

        if self.gpx_file != "":
            self.parse()

    def checkSchema(self):
        pass

    def parse(self, gpx_file: str = ""):
        
        # File
        if gpx_file != "":
            self.gpx_file = gpx_file
        elif self.gpx_file == "":
            logging.error("No GPX file to parse")
            return

        # Parse GPX file
        try:
            self.gpx_tree = ET.parse(self.gpx_file)
            self.gpx_root = self.gpx_tree.getroot()
        except:
            logging.exception("Unable to parse GPX file")
            raise
        
        # Parse metadata
        try:
            self.parseMetadata()
        except:
            logging.exception("Unable to parse metadata in GPX file")
            raise

        # Parse tracks
        try:
            self.parseTracks()
        except:
            logging.exception("Unable to parse tracks in GPX file")
            raise

        logging.debug("Parsing complete")

    def parseMetadata(self):
        pass

    def parseTracks(self):

        # Tracks
        tracks = self.gpx_root.findall("topo:trk", self.name_space)
        for track in tracks:
            name = track.find("topo:name", self.name_space)
            segments = track.findall("topo:trkseg", self.name_space)

            # Create new track
            gpx_track = Track(name=name)

            # Track segments
            for segment in segments:
                points = segment.findall("topo:trkpt", self.name_space)

                # Crete new segment
                gpx_segment = TrackSegment()

                # Track points
                for point in points:
                    elevation = point.find("topo:ele", self.name_space)
                    time = point.find("topo:time", self.name_space)
                    
                    # Create new point
                    gpx_point = TrackPoint(point.get("lat"), point.get("lon"), elevation.text, time.text)

                    gpx_segment.track_points.append(gpx_point)

                gpx_track.track_segments.append(gpx_segment)
            
            self.gpx.tracks.append(gpx_track)