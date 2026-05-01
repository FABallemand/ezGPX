# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Extensions class.
"""

import os
import sys

import pytest

FILE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.realpath(os.path.dirname(FILE_DIR))  # Main folder

os.chdir(FILE_DIR)
sys.path.append(PARENT_DIR + "/ezgpx")

from ezgpx import Extensions  # pylint: disable=wrong-import-position


class TestExtensions:

    @pytest.mark.parametrize(
        "values, tag",
        [
            pytest.param({}, "t", id="empty"),
            pytest.param({"k1": "v1", "k2": "v2"}, "t", id="dict_1"),
            pytest.param({"k1": 1, "k2": 2}, "t", id="dict_2"),
            pytest.param({1: "v1", 2: "v2"}, "t", id="dict_3"),
            pytest.param(
                {"k1": {"k11": "v11", "k12": "v12"}, "k2": {"k21": "v21"}},
                "t",
                id="dict_4",
            ),
        ],
    )
    def test_valid_values(self, values, tag):
        e = Extensions(values, tag)
        assert isinstance(e.values, dict)
        assert isinstance(e.tag, str)
        assert e.values == values
        assert e.tag == "t"

    @pytest.mark.parametrize(
        "values, tag",
        [
            pytest.param(42, "t", id="int"),
            pytest.param(3.14, "t", id="float"),
            pytest.param("a", "t", id="str"),
            pytest.param([], "t", id="list"),
        ],
    )
    def test_invalid_values_raise(self, values, tag):
        with pytest.raises(TypeError):
            Extensions(values, tag)

    def test_default_values(self):
        e = Extensions()
        assert e.values is None
        assert e.tag == "extensions"

    def test_fields(self):
        assert Extensions._fields == []

    def test_mandatory_fields(self):
        assert Extensions._mandatory_fields == []
