from datetime import datetime

from .link import Link

class Metadata():
    """
    Metadata (metadata) element in GPX file.
    """

    def __init__(
            self,
            name: str = None,
            desc: str = None,
            author: str = None,
            copyright: str = None,
            link: Link = None,
            time: datetime = None,
            keywords: str = None,
            bounds: str = None,
            extensions: str = None):
        self.name: str = name,
        self.desc: str = desc,
        self.author: str = author,
        self.copyright: str = copyright,
        self.link: Link = link,
        self.time: datetime = time,
        self.keywords: str = keywords,
        self.bounds: str = bounds,
        self.extensions: str = extensions