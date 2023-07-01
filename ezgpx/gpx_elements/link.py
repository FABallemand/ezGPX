

class Link():
    """
    Link (link) element in GPX file.
    """

    def __init__(
            self,
            href: str = None,
            text: str = None,
            type: str = None) -> None:
        """
        Initialize Link instance.

        Args:
            href (str, optional): Hyper reference. Defaults to None.
            text (str, optional): Text. Defaults to None.
            type (str, optional): Type. Defaults to None.
        """
        self.href: str = href
        self.text: str = text
        self.type: str = type
        
