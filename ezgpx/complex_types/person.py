"""
This module contains the Person class.
"""

from dataclasses import dataclass
from typing import ClassVar

from .email import Email
from .link import Link


@dataclass
class Person:
    """
    personType: A person or organization.

    Args:
        name (str, optional): Name of person or organization.
            Defaults to None.
        email (Email, optional): Email address. Defaults to None.
        link (Link, optional): Link to Web site or other external
            information about person. Defaults to None.
        tag (str, optional): XML tag. Defaults to "person".
    """

    name: str = None
    email: Email = None
    link: Link = None
    tag: str = "author"

    _fields: ClassVar[list[str]] = ["name", "email", "link"]
    _mandatory_fields: ClassVar[list[str]] = []

    def __post_init__(self):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)
        if self.email is not None and not isinstance(self.email, Email):
            raise TypeError("`email` must be of type Email")
        if self.link is not None and not isinstance(self.link, Link):
            raise TypeError("`link` must be of type Link")
        if not isinstance(self.tag, str):
            self.tag = str(self.tag)
