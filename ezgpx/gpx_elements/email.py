
class Email():
    """
    emailType element in GPX file.
    """

    def __init__(
            self,
            tag: str = "email",
            id: str = None,
            domain: str = None) -> None:
        """
        Initialize Email instance.

        Parameters
        ----------
        tag : str, optional
            XML tag, by default "email"
        id : str, optional
            Identifier, by default None
        domain : str, optional
            Domain, by default None
        """
        self.tag: str = tag
        self.id: str = id
        self.domain: str = domain