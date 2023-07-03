
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

        Args:
            tag (str, optional): XML tag. Defaults to "email".
            id (str, optional): Identifier. Defaults to None.
            domain (str, optional): Domain. Defaults to None.
        """
        self.tag: str = tag
        self.id: str = id
        self.domain: str = domain