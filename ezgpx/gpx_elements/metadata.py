from datetime import datetime

from .link import Link
from .person import Person

class Metadata():
    """
    metadataType element in GPX file.
    """

    def __init__(
            self,
            tag: str = "metadata",
            name: str = None,
            desc: str = None,
            author: Person = None,
            copyright: str = None,
            link: Link = None,
            time: datetime = None,
            keywords: str = None,
            bounds: str = None,
            extensions: str = None) -> None:
        """
        Initialize Metadata instance.

        Args:
            tag (str, optional): XML tag. Defaults to "metadata".
            name (str, optional): Name. Defaults to None.
            desc (str, optional): Description. Defaults to None.
            author (Person, optional): Author. Defaults to None.
            copyright (str, optional): Copyright. Defaults to None.
            link (Link, optional): Link. Defaults to None.
            time (datetime, optional): Time. Defaults to None.
            keywords (str, optional): Keywords. Defaults to None.
            bounds (str, optional): Bounds. Defaults to None.
            extensions (str, optional): Extensions. Defaults to None.
        """
        self.tag: str = tag
        self.name: str = name
        self.desc: str = desc
        self.author: Person = author
        self.copyright: str = copyright
        self.link: Link = link
        self.time: datetime = time
        self.keywords: str = keywords
        self.bounds: str = bounds
        self.extensions: str = extensions