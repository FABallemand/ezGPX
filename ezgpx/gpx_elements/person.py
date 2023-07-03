from .email import Email
from .link import Link

class Person():
    """
    personType element in GPX file.
    """

    def __init__(
            self,
            tag: str = "person",
            name: str = None,
            email: Email = None,
            link: Link = None) -> None:
        """
        Initialize Person instance.

        Args:
            tag (str, optional): XML tag. Defaults to "person".
            name (str, optional): Name. Defaults to None.
            email (Email, optional): Email. Defaults to None.
            link (Link, optional): Link. Defaults to None.
        """
        self.tag: str = tag
        self.name: str = name
        self.email: Email = email
        self.link: Link = link