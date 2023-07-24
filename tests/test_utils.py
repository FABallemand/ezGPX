import sys
import os
import pytest
from shutil import rmtree

import numpy as np
import math
import matplotlib.pyplot as plt

file_folder = os.path.dirname(__file__)
parent_folder = os.path.realpath(os.path.dirname(file_folder)) # ie: ezGPX

os.chdir(file_folder)
sys.path.append(parent_folder + "/ezgpx")

from ezgpx import utils, WayPoint

class TestUtils():

    def test_haversine_distance(self):
        point_1 = WayPoint("wpt", 48.0, 2.0)
        point_2 = WayPoint("wpt", 43.0, 5.0)
        assert math.isclose(utils.haversine_distance(point_1, point_2), 603020.0, abs_tol=1000.0)

    def _test_perpendicular_distance_horizontal_line(self):
        start = WayPoint("wpt", 0, 0)
        end = WayPoint("wpt", 0, 2)
        point = WayPoint("wpt", 1, 1)
        return math.isclose(utils.perpendicular_distance(start, end, point), 1)

    def _test_perpendicular_distance_vertical_line(self):
        start = WayPoint("wpt", 0, 0)
        end = WayPoint("wpt", 2, 0)
        point = WayPoint("wpt", 1, 1)
        return math.isclose(utils.perpendicular_distance(start, end, point), 1)
    
    def _test_perpendicular_distance_random_line(self):
        start = WayPoint("wpt", 0, 0)
        end = WayPoint("wpt", 1, 1)
        point = WayPoint("wpt", 1, 0)
        return math.isclose(utils.perpendicular_distance(start, end, point), math.sqrt(2)/2)
    
    def _test_perpendicular_distance_point_on_line(self):
        start = WayPoint("wpt", 0, 0)
        end = WayPoint("wpt", 1, 1)
        point = WayPoint("wpt", 2, 2)
        return math.isclose(utils.perpendicular_distance(start, end, point), 0)
    
    def test_perpendicular_distance(self):
        assert self._test_perpendicular_distance_horizontal_line()
        assert self._test_perpendicular_distance_vertical_line()
        assert self._test_perpendicular_distance_random_line()
        assert self._test_perpendicular_distance_point_on_line()
