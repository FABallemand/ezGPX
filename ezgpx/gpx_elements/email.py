
class Email():
    """
    Email (email) element in GPX file.
    """

    def __init__(
            self,
            id: str = None,
            domain: str = None) -> None:
        """
        Initialize Email instance.

        Args:
            id (str, optional): Identifier. Defaults to None.
            domain (str, optional): Domain. Defaults to None.
        """
        self.id: str = id
        self.domain: str = domain