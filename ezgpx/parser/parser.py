from typing import Dict, Optional, Union
import logging

from ..gpx_elements import Gpx

DEFAULT_PRECISION = 10
DEFAULT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

class Parser():
    """
    File parser.
    """

    def __init__(
            self,
            file_path: Optional[str] = None,
            name_spaces: Dict = None) -> None:
        """
        Initialize Parser instance.

        Args:
            file_path (str, optional): Path to the file to parse. Defaults to None.
        """
        self.file_path: str = file_path

        self.ele_data: bool = False
        self.time_data:bool = False
        self.precisions: dict = {
            "lat_lon": DEFAULT_PRECISION,
            "elevation": DEFAULT_PRECISION,
            "distance": DEFAULT_PRECISION,
            "duration": DEFAULT_PRECISION,
            "speed": DEFAULT_PRECISION,
            "rate": DEFAULT_PRECISION,
            "default": DEFAULT_PRECISION
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
        
        if type(number) == int:
            return 0
        elif type(number) == float:
            number = str(number)
        elif type(number) == str:
            try:
                test = float(number)
            except OSError as err:
                logging.exception(f"OS error: {err}")
            except ValueError:
                logging.exception("Could not convert data ({number}) to a floating point value.")
            except Exception as err:
                logging.exception(f"Unexpected {err}, {type(err)}.\nUnable to find precision of number: {number}")
                raise

        if "." in number:
            _, decimal = number.split(sep=".")
            return len(decimal)
        else:
            return 0