import logging
from datetime import datetime

import xml.etree.ElementTree as ET

from ..gpx_elements import Gpx, Metadata, Track, TrackSegment, TrackPoint

class Parser():

    def __init__(self, file_path: str = ""):
        self.file_path = file_path
        self.gpx_tree = None
        self.gpx_root = None
        self.name_space = {"topo": "http://www.topografix.com/GPX/1/1"}
        self.gpx = Gpx()

        if self.file_path != "":
            self.parse()

    def check_schema(self):
        pass

    def parse_metadata(self):
        pass

    def parse_tracks(self):

        # Tracks
        tracks = self.gpx_root.findall("topo:trk", self.name_space)
        for track in tracks:
            name = track.find("topo:name", self.name_space)
            segments = track.findall("topo:trkseg", self.name_space)

            # Create new track
            gpx_track = Track(name=name.text)

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
                    gpx_point = TrackPoint(float(point.get("lat")),
                                           float(point.get("lon")),
                                           float(elevation.text),
                                           datetime.strptime(time.text, "%Y-%m-%dT%H:%M:%SZ"))

                    gpx_segment.track_points.append(gpx_point)

                gpx_track.track_segments.append(gpx_segment)
            
            self.gpx.tracks.append(gpx_track)

    def parse(self, file_path: str = "") -> Gpx:
        
        # File
        if file_path != "":
            self.file_path = file_path
        elif self.file_path == "":
            logging.error("No GPX file to parse")
            return

        # Parse GPX file
        try:
            self.gpx_tree = ET.parse(self.file_path)
            self.gpx_root = self.gpx_tree.getroot()
        except:
            logging.exception("Unable to parse GPX file")
            raise
        
        # Parse metadata
        try:
            self.parse_metadata()
        except:
            logging.exception("Unable to parse metadata in GPX file")
            raise

        # Parse tracks
        try:
            self.parse_tracks()
        except:
            logging.exception("Unable to parse tracks in GPX file")
            raise

        logging.debug("Parsing complete")
        return self.gpx