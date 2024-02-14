from .gpx import GPX


def merge(gpx_1: GPX, gpx_2: GPX) -> GPX:

    # Create new GPX instance
    merged_gpx = GPX()

    # Fill new GPX instance
    merged_gpx.gpx.tag = "gpx"
    merged_gpx.gpx.creator = "ezGPX"
    merged_gpx.gpx.xmlns = "http://www.topografix.com/GPX/1/1"
    merged_gpx.gpx.version = "1.1"
    merged_gpx.gpx.xmlns_xsi = "http://www.w3.org/2001/XMLSchema-instance"
    merged_gpx.gpx.xsi_schema_location = ["http://www.topografix.com/GPX/1/1", "http://www.topografix.com/GPX/1/1/gpx.xsd"]
    merged_gpx.gpx.xmlns_gpxtpx = None #TODO
    merged_gpx.gpx.xmlns_gpxtrk = None #TODO
    merged_gpx.gpx.xmlns_wptx1 = None #TODO
    merged_gpx.gpx.metadata = None #TODO
    merged_gpx.gpx.wpt = gpx_1.gpx.wpt + gpx_2.gpx.wpt
    merged_gpx.gpx.rte = gpx_1.gpx.rte + gpx_2.gpx.rte
    merged_gpx.gpx.tracks = gpx_1.gpx.tracks + gpx_2.gpx.tracks
    merged_gpx.gpx.extensions = None #TODO

    # Return new GPX instance
    return merged_gpx
