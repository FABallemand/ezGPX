from .email import Email
from .gpx_element import GpxElement
from .link import Link

class Person(GpxElement):
    """
    personType element in GPX file.
    """
    fields = ["name", "email", "link"]
    mandatory_fields = []

    def __init__(
            self,
            tag: str = "person",
            name: str = None,
            email: Email = None,
            link: Link = None) -> None:
        """
        Initialize Person instance.

        Parameters
        ----------
        tag : str, optional
            XML tag, by default "person"
        name : str, optional
            Name, by default None
        email : Email, optional
            Email, by default None
        link : Link, optional
            Link, by default None
        """
        self.tag: str = tag
        self.name: str = name
        self.email: Email = email
        self.link: Link = link