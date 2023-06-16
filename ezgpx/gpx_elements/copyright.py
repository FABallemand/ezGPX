
class Copyright():
    """
    Copyright (copyright) element in GPX file.
    """

    def __init__(
            self,
            author: str = None,
            year: int = None,
            licence: str = None) -> None:
        self.author: str = author
        self.year: int = year
        self.licence: str = licence
        