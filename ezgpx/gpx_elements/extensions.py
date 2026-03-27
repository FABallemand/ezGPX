"""
This module contains the Extensions class.
"""

from .gpx_element import GpxElement


class Extensions(GpxElement):
    """
    extensionsType element in GPX file.
    """

    fields = []
    mandatory_fields = []

    def __init__(self, tag: str = "extensions", values: dict = None) -> None:
        """
        Initialise Extensions instance.

        Args:
            tag (str, optional): XML tag. Defaults to "extensions".
            values (dict, optional): Extension content. Defaults to None.
        """
        self.tag: str = tag
        self.values: dict = values if values is not None else {}
