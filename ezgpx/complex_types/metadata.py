"""
This module contains the Metadata class.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from .bounds import Bounds
from .copyright import Copyright
from .extensions import Extensions
from .link import Link
from .person import Person


@dataclass
class Metadata:  # pylint: disable=too-many-instance-attributes
    """
    metadataType: Information about the GPX file, author, and copyright
    restrictions goes in the metadata section. Providing rich,
    meaningful information about your GPX files allows others to search
    for and use your GPS data.

    Args:
        name (str, optional): Name of the GPX file. Defaults to None.
        desc (str, optional): Description of the contents of the GPX
            file. Defaults to None.
        author (Person, optional): Person or organization who created
            the GPX file. Defaults to None.
        copyright (str, optional): Copyright and license information
            governing use of the file. Defaults to None.
        link (list[Link], optional): URLs associated with the location
            described in the file. Defaults to None.
        time (datetime, optional): Creation date of the file.
            Defaults to None.
        keywords (str, optional): Keywords associated with the file.
            Search engines or databases can use this information to
            classify the data. Defaults to None.
        bounds (str, optional): Minimum and maximum coordinates which
            describe the extent of the coordinates in the file.
            Defaults to None.
        extensions (Extensions, optional): You can add extend GPX by
            adding your own elements from another schema here.
            Defaults to None.
        tag (str, optional): XML tag. Defaults to "metadata".
    """

    name: str = None
    desc: str = None
    author: Person = None
    copyright: Copyright = None
    link: list[Link] = None
    time: datetime = None
    keywords: str = None
    bounds: Bounds = None
    extensions: Extensions = None
    tag: str = "metadata"

    _fields: ClassVar[list[str]] = [
        "name",
        "desc",
        "author",
        "copyright",
        "link",
        "time",
        "keywords",
        "bounds",
        "extensions",
    ]
    _mandatory_fields: ClassVar[list[str]] = []

    def __post_init__(self):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)
        if self.desc is not None and not isinstance(self.desc, str):
            self.desc = str(self.desc)
        if self.author is not None and not isinstance(self.author, Person):
            raise TypeError("`author` must be of type Person")
        if self.copyright is not None and not isinstance(self.copyright, Copyright):
            raise TypeError("`copyright` must be of type Copyright")
        if self.link is not None and (
            not isinstance(self.link, list)
            or not all(isinstance(ll, Link) for ll in self.link)
        ):
            raise TypeError("`link` must be of type list[Link]")
        if self.time is not None and not isinstance(self.time, datetime):
            raise TypeError("`time` must be of type datetime")
        if self.keywords is not None and not isinstance(self.keywords, str):
            self.keywords = str(self.keywords)
        if self.bounds is not None and not isinstance(self.bounds, Bounds):
            raise TypeError("`bounds` must be of type Bounds")
        if self.extensions is not None and not isinstance(self.extensions, Extensions):
            raise TypeError("`extensions` must be of type Extensions")
        if not isinstance(self.tag, str):
            self.tag = str(self.tag)
