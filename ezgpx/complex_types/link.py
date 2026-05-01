"""
This module contains the Link class.
"""

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Link:
    """
    linkType: A link to an external resource (Web page, digital photo,
    video clip, etc) with additional information.

    Args:
        href (str):URL of hyperlink.
        text (str, optional): Text of hyperlink. Defaults to None.
        type (str, optional): Mime type of content (image/jpeg).
            Defaults to None.
        tag (str, optional): XML tag. Defaults to "link".
    """

    href: str
    text: str = None
    type: str = None
    tag: str = "link"

    _fields: ClassVar[list[str]] = ["href", "text", "type"]
    _mandatory_fields: ClassVar[list[str]] = ["href"]

    def __post_init__(self):
        if not isinstance(self.href, str):
            self.href = str(self.href)
        if self.text is not None and not isinstance(self.text, str):
            self.text = str(self.text)
        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)
        if not isinstance(self.tag, str):
            self.tag = str(self.tag)
