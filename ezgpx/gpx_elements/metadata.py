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

        Parameters
        ----------
        tag : str, optional
            XML tag, by default "metadata"
        name : str, optional
            Name, by default None
        desc : str, optional
            Description, by default None
        author : Person, optional
            Author, by default None
        copyright : str, optional
            Copyright, by default None
        link : Link, optional
            Link, by default None
        time : datetime, optional
            Time, by default None
        keywords : str, optional
            Keywords, by default None
        bounds : str, optional
            Bounds, by default None
        extensions : str, optional
            Extensions, by default None
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