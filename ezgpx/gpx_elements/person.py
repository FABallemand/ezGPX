from .email import Email
from .link import Link

class Person():
    """
    Person (person) element in GPX file.
    """

    def __init__(
            self,
            name: str = None,
            email: Email = None,
            link: Link = None) -> None:
        """
        Initialize Person instance.

        Args:
            name (str, optional): Name. Defaults to None.
            email (Email, optional): Email. Defaults to None.
            link (Link, optional): Link. Defaults to None.
        """
        self.name: str = name
        self.email: Email = email
        self.link: Link = link