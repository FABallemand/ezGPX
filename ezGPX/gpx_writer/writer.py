import xml.etree.ElementTree as ET

from ..gpx_elements import GPX

class Writer():

    def __init__(self, gpx: GPX = None, path: str = "", metadata: bool = True, ele: bool = True, time: bool = True):
        
        self.gpx = gpx
        self.path = path
        self.gpx_string = ""

        # Parameters
        self.metadata = metadata
        self.ele = ele
        self.time = time

        self.write()


    def write(self, gpx: GPX = None, path: str = "", metadata: bool = True, ele: bool = True, time: bool = True):
        
        if gpx is not None:
            self.gpx = gpx

        if path != "":
            self.path = path

        if self.gpx is not None:
            self.GPXtoString()

        # Is it smart ??
        self.metadata = metadata
        self.ele = ele
        self.time = time

        if self.path != "": # + Check if path is correct
            self.writeGPX()


    def GPXtoString(self, gpx: GPX = None, metadata: bool = True, ele: bool = True, time: bool = True) -> str:

        if gpx is not None:
            self.gpx = gpx

        # Is it smart ??
        self.metadata = metadata
        self.ele = ele
        self.time = time

        if self.gpx is not None:
            # Root
            gpx_root = ET.Element("gpx")

            # Metadata
            if self.metadata:
                pass

            # Tracks
            for gpx_track in self.gpx.tracks:
                track = ET.SubElement(gpx_root, "trk")

                # Track segments
                for gpx_segment in gpx_track.track_segments:
                    segment = ET.SubElement(track, "trkseg")

                    # Track points
                    for gpx_point in gpx_segment.track_points:
                        point = ET.SubElement(segment, "trkpt")
                        point.set("lat", gpx_point.lat)
                        point.set("lon", gpx_point.lat)
                        if self.ele:
                            ele = ET.SubElement(point, "ele")
                            ele.text = str(gpx_point.ele)
                        if self.time:
                            time = ET.SubElement(point, "time")
                            time.text = gpx_point.time


            # Convert data to string
            self.gpx_string = ET.tostring(gpx_root)

            return self.gpx_string

    def writeGPX(self, path: str = ""):

        if path != "":
            self.path = path

        if self.path != "":
            # Write GPX file
            with open(self.path, "wb") as f:
                f.write(self.gpx_string)

