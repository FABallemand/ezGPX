# pylint: disable=missing-class-docstring, missing-function-docstring, protected-access
"""
This module contains tests for the Parser class.
"""

import os
import sys

FILE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.realpath(os.path.dirname(FILE_DIR))  # Main folder

os.chdir(FILE_DIR)
sys.path.append(PARENT_DIR + "/ezgpx")

import pytest

from ezgpx import DEFAULT_PRECISION, Parser  # pylint: disable=wrong-import-position


class TestParser:

    @pytest.mark.parametrize(
        "number,expected",
        [
            pytest.param(
                None,
                DEFAULT_PRECISION,
                id="None",
            ),
            pytest.param(
                "0",
                0,
                id="Integer",
            ),
            pytest.param(
                "0.0",
                1,
                id="Float",
            ),
        ],
    )
    def test_find_precision(self, benchmark, number, expected):
        parser = Parser("", None)
        result = benchmark(parser._find_precision, number)
        assert result == expected

    # def test_find_time_format():  # TODO
