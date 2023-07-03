

class Link():
    """
    linkType element in GPX file.
    """

    def __init__(
            self,
            tag: str = "link",
            href: str = None,
            text: str = None,
            type: str = None) -> None:
        """
        Initialize Link instance.

        Args:
            tag (str, optional): XML tag. Defaults to "link".
            href (str, optional): Hyper reference. Defaults to None.
            text (str, optional): Text. Defaults to None.
            type (str, optional): Type. Defaults to None.
        """
        self.tag: str = tag
        self.href: str = href
        self.text: str = text
        self.type: str = type
        
