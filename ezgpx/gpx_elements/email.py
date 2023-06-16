
class Email():
    """
    Email (email) element in GPX file.
    """

    def __init__(
            self,
            id: str = None,
            domain: str = None) -> None:
        self.id: str = id
        self.domain: str = domain