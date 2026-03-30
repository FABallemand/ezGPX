"""
This module contains the GpxElement class.
"""


class GpxElement:
    """
    Base class for element in GPX file.
    Implements dunders functions.
    """

    fields = []
    mandatory_fields = []

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}[{self.tag}]("
            + ", ".join(str(getattr(self, a)) for a in self.mandatory_fields)
            + ")"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}[{self.tag}]("
            + ", ".join(repr(getattr(self, a)) for a in self.mandatory_fields)
            + ")"
        )
