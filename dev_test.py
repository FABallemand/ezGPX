import sys, os
import logging

from ezGPX.gpx_parser import Parser
from ezGPX.gpx_writer import Writer

if __name__ == "__main__":

    # Log file
    log_file = "dev_tests.log"
    if os.path.exists(log_file):
        os.remove(log_file)
    logging.basicConfig(filename=log_file, encoding="utf-8", level=logging.DEBUG)

    gpx_parser = Parser("test_files/garmin_etrex_1.gpx")
    gpx_writer = Writer(gpx_parser.gpx, "test_files/garmin_etrex_1_test.gpx")