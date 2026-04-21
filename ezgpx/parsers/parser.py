"""
This module contains the Parser class.
"""

import io
import warnings
from datetime import datetime
from pathlib import Path
from typing import IO

from ..constants.precisions import (
    DEFAULT_PRECISION,
    DEFAULT_PRECISION_DICT,
    DEFAULT_TIME_FORMAT,
    POSSIBLE_TIME_FORMATS,
)
from ..gpx_elements import Gpx


class Parser:
    """
    File parser.
    """

    def __init__(
        self, source: str | Path | IO[str] | IO[bytes] | bytes, name_spaces: dict = None
    ) -> None:
        """
        Initialise Parser instance.

        Args:
            source (str | Path | IO[str] | IO[bytes] | bytes): Path to a
                file or a file-like object to parse.
        """
        # Bytes object
        if isinstance(source, bytes):
            source = io.BytesIO(source)
        self.source: str | Path | IO[str] | IO[bytes] = source

        self.ele_data: bool = False
        self.time_data: bool = False
        self.precisions: dict = DEFAULT_PRECISION_DICT
        self.time_format: str = DEFAULT_TIME_FORMAT

        self.gpx: Gpx = Gpx(xmlns=name_spaces)

    def _find_precision(self, number: str | None) -> int:
        """
        Find decimal precision of a given number.

        Args:
            number (str | None): Number.

        Returns:
            int: Decimal precision.
        """
        if number is None:
            return DEFAULT_PRECISION
        if "." in number:
            _, decimal = number.split(sep=".")
            return len(decimal)
        return 0

    def _find_time_format(self, time: str | None):
        """
        Find time format used in the source file.

        Args:
            time (str | None): Time.
        """
        self.time_data = time is not None

        for tf in POSSIBLE_TIME_FORMATS:
            try:
                datetime.strptime(time, tf)
                self.time_format = tf
                break
            except (TypeError, ValueError):  # time is None, wrong time format
                pass
        else:
            warnings.warn("Unknown time format. Default time format will be used.")
