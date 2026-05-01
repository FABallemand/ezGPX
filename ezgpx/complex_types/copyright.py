"""
This module contains the Copyright class.
"""

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Copyright:
    """
    copyrightType: Information about the copyright holder and any
    license governing use of this file. By linking to an appropriate
    license, you may place your data into the public domain or grant
    additional usage rights.

    Args:
        author (str): Copyright holder.
        year (int, optional): Year of copyright. Defaults to None.
        licence (str, optional): Link to external file containing
            license text. Defaults to None.
        tag (str, optional): XML tag. Defaults to "copyright".
    """

    author: str
    year: int = None
    license: str = None
    tag: str = "copyright"

    _fields: ClassVar[list[str]] = ["author", "year", "licence"]
    _mandatory_fields: ClassVar[list[str]] = ["author"]

    def __post_init__(self):
        if not isinstance(self.author, str):
            self.author = str(self.author)
        if self.year is not None and not isinstance(self.year, int):
            self.year = int(self.year)
        if self.license is not None and not isinstance(self.license, str):
            self.license = str(self.license)
        if not isinstance(self.tag, str):
            self.tag = str(self.tag)

        if self.year is not None and self.year < 0:
            raise ValueError("`year` must be a valid year.")
