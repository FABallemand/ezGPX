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

from ezgpx import Wpt, utils  # pylint: disable=wrong-import-position


class TestUtils:

    def test_haversine_distance(self, benchmark):
        result = benchmark(
            utils.haversine_distance,
            Wpt(48.0, 2.0),
            Wpt(43.0, 5.0),
        )
        assert result == pytest.approx(603020.0)

    @pytest.mark.parametrize(
        "start,end,point,expected",
        [
            pytest.param(
                Wpt(0, 0),
                Wpt(0, 2),
                Wpt(1, 1),
                1.0,
                id="horizontal_line",
            ),
            pytest.param(
                Wpt(0, 0),
                Wpt(2, 0),
                Wpt(1, 1),
                1.0,
                id="vertical_line",
            ),
            pytest.param(
                Wpt(0, 0),
                Wpt(1, 1),
                Wpt(1, 0),
                math.sqrt(2) / 2,
                id="diagonal_line",
            ),
            pytest.param(
                Wpt(0, 0),
                Wpt(1, 1),
                Wpt(2, 2),
                0.0,
                id="point_on_line",
            ),
        ],
    )
    def test_perpendicular_distance(self, benchmark, start, end, point, expected):
        result = benchmark(utils.perpendicular_distance, start, end, point)
        assert result == pytest.approx(expected)
