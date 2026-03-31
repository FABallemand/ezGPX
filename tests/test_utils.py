# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the utility functions.
"""

import math
import os
import sys

import pytest

file_folder = os.path.dirname(__file__)
parent_folder = os.path.realpath(os.path.dirname(file_folder))  # ie: ezGPX

os.chdir(file_folder)
sys.path.append(parent_folder + "/ezgpx")

from ezgpx import WayPoint, utils


class TestUtils:
    def test_haversine_distance(self, benchmark):
        result = benchmark(
            utils.haversine_distance,
            WayPoint("wpt", 48.0, 2.0),
            WayPoint("wpt", 43.0, 5.0),
        )
        assert result == pytest.approx(603020.0)

    @pytest.mark.parametrize(
        "start,end,point,expected",
        [
            pytest.param(
                WayPoint("wpt", 0, 0),
                WayPoint("wpt", 0, 2),
                WayPoint("wpt", 1, 1),
                1.0,
                id="horizontal_line",
            ),
            pytest.param(
                WayPoint("wpt", 0, 0),
                WayPoint("wpt", 2, 0),
                WayPoint("wpt", 1, 1),
                1.0,
                id="vertical_line",
            ),
            pytest.param(
                WayPoint("wpt", 0, 0),
                WayPoint("wpt", 1, 1),
                WayPoint("wpt", 1, 0),
                math.sqrt(2) / 2,
                id="diagonal_line",
            ),
            pytest.param(
                WayPoint("wpt", 0, 0),
                WayPoint("wpt", 1, 1),
                WayPoint("wpt", 2, 2),
                0.0,
                id="point_on_line",
            ),
        ],
    )
    def test_perpendicular_distance(self, benchmark, start, end, point, expected):
        result = benchmark(utils.perpendicular_distance, start, end, point)
        assert result == pytest.approx(expected)
