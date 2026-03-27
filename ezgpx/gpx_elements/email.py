"""
This module contains the Email class.
"""

from .gpx_element import GpxElement


class Email(GpxElement):
    """
    emailType element in GPX file.
    """

    fields = ["id", "domain"]
    mandatory_fields = ["id", "domain"]

    def __init__(
        self,
        tag: str = "email",
        id: str = None,  # pylint: disable=redefined-builtin
        domain: str = None,
    ) -> None:
        """
        Initialise Email instance.

        Args:
            tag (str, optional): XML tag. Defaults to "email".
            id (str, optional): Identifier. Defaults to None.
            domain (str, optional): Domain. Defaults to None.
        """
        self.tag: str = tag
        self.id: str = id
        self.domain: str = domain
