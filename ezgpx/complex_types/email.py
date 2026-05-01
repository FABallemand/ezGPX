"""
This module contains the Email class.
"""

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Email:
    """
    emailType: An email address. Broken into two parts (id and domain)
    to help prevent email harvesting.

    Args:
        id (str): identifier (half of email address).
        domain (str): Domain (half of email address).
        tag (str, optional): XML tag. Defaults to "email".
    """

    id: str
    domain: str
    tag: str = "email"

    _fields: ClassVar[list[str]] = ["id", "domain"]
    _mandatory_fields: ClassVar[list[str]] = ["id", "domain"]

    def __post_init__(self):
        if not isinstance(self.id, str):
            self.id = str(self.id)
        if not isinstance(self.domain, str):
            self.domain = str(self.domain)
        if not isinstance(self.tag, str):
            self.tag = str(self.tag)
