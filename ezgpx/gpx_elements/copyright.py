"""
This module contains the Copyright class.
"""

from .gpx_element import GpxElement


class Copyright(GpxElement):
    """
    copyrightType element in GPX file.
    """

    fields = ["author", "year", "licence"]
    mandatory_fields = ["author"]

    def __init__(
        self,
        tag: str = "copyright",
        author: str = None,
        year: int = None,
        licence: str = None,
    ) -> None:
        """
        Initialise Copyright instance.

        Args:
            tag (str, optional): XML tag. Defaults to "copyright".
            author (str, optional): Author. Defaults to None.
            year (int, optional): Year. Defaults to None.
            licence (str, optional): Licence. Defaults to None.
        """
        self.tag: str = tag
        self.author: str = author
        self.year: int = year
        self.licence: str = licence
