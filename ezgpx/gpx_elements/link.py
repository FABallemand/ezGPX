

class Link():
    """
    Link (link) element in GPX file.
    """

    def __init__(
            self,
            href: str = None,
            text: str = None,
            type: str = None) -> None:
        self.href: str = href
        self.text: str = text
        self.type: str = type
        
