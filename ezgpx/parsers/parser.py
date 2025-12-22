"""
This module contains the Parser class.
"""

import warnings
from pathlib import Path
from typing import IO, Dict, Union

from ..constants.precisions import DEFAULT_PRECISION, DEFAULT_TIME_FORMAT
from ..gpx_elements import Gpx


class Parser:
    """
    File parser.
    """

    def __init__(
        self, source: str | Path | IO[str] | IO[bytes] | bytes, name_spaces: Dict = None
    ) -> None:
        """
        Initialise Parser instance.

        Args:
            source (str | Path | IO[str] | IO[bytes] | bytes): Path to a
                file or a file-like object to parse.
        """
        self.source: str = source

        self.ele_data: bool = False
        self.time_data: bool = False
        self.precisions: dict = {
            "lat_lon": DEFAULT_PRECISION,
            "elevation": DEFAULT_PRECISION,
            "distance": DEFAULT_PRECISION,
            "duration": DEFAULT_PRECISION,
            "speed": DEFAULT_PRECISION,
            "rate": DEFAULT_PRECISION,
            "default": DEFAULT_PRECISION,
        }
        self.time_format: str = DEFAULT_TIME_FORMAT

        self.gpx: Gpx = Gpx(xmlns=name_spaces)

    def find_precision(self, number: Union[int, float, str]) -> int:
        """
        Find decimal precision of a given number.

        Parameters
        ----------
        number : Union[int, float, str]
            Number.

        Returns
        -------
        int
            Decimal precision.
        """
        if number is None:
            return DEFAULT_PRECISION

        if isinstance(number, int):
            return 0
        elif isinstance(number, float):
            number = str(number)
        elif isinstance(number, str):
            try:
                float(number)
            except OSError as err:
                warnings.warn("OS error: %s", err)
            except ValueError:
                warnings.warn(
                    "Could not convert data (%s) to a floatingpoint value.", number
                )
            except Exception as err:
                warnings.warn(
                    "Unexpected %s, %s.Unable to find precision of number: %s",
                    err,
                    type(err),
                    number,
                )
                raise

        if "." in number:
            _, decimal = number.split(sep=".")
            return len(decimal)
        return 0
