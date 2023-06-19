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
        self.name: str = name
        self.email: Email = email
        self.link: Link = link