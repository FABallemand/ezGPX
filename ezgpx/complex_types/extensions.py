"""
This module contains the Extensions class.
"""

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Extensions:
    """
    extensionsType: You can add extend GPX by adding your own elements
    from another schema here.

    Args:
        values (dict, optional): Extension content. Defaults to None.
        tag (str, optional): XML tag. Defaults to "extensions".
    """

    values: dict = None
    tag: str = "extensions"

    _fields: ClassVar[list[str]] = []
    _mandatory_fields: ClassVar[list[str]] = []

    def __post_init__(self):
        if self.values is not None and not isinstance(self.values, dict):
            raise TypeError("`values` must be of type dict")
        if not isinstance(self.tag, str):
            self.tag = str(self.tag)
