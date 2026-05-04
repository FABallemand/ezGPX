# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Email class.
"""

import os
import sys

import pytest

FILE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.realpath(os.path.dirname(FILE_DIR))  # Main folder

os.chdir(FILE_DIR)
sys.path.append(PARENT_DIR + "/ezgpx")

from ezgpx import Email  # pylint: disable=wrong-import-position


class TestEmail:

    @pytest.mark.parametrize(
        "id, domain, tag",
        [
            pytest.param("test-id", "test-domain", "t", id="1"),
        ],
    )
    def test_valid_values(self, id, domain, tag):  # pylint: disable=redefined-builtin
        e = Email(id, domain, tag)
        assert isinstance(e.id, str)
        assert isinstance(e.domain, str)
        assert isinstance(e.tag, str)
        assert e.id == "test-id"
        assert e.domain == "test-domain"
        assert e.tag == "t"

    # @pytest.mark.parametrize(
    #     "id, domain, tag",
    #     [
    #         pytest.param("test-id", "test-domain", "t", id="none"),
    #     ],
    # )
    # def test_invalid_values_raise(self, id, domain, tag):  # pylint: disable=redefined-builtin
    #     with pytest.raises((TypeError, ValueError)):
    #         Email(id, domain, tag)

    def test_default_tag(self):
        e = Email(
            id="test-id",
            domain="test-domain",
        )
        assert e.tag == "email"

    def test_fields(self):
        assert Email._fields == ["id", "domain"]

    def test_mandatory_fields(self):
        assert Email._mandatory_fields == ["id", "domain"]
