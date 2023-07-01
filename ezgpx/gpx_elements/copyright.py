
class Copyright():
    """
    Copyright (copyright) element in GPX file.
    """

    def __init__(
            self,
            author: str = None,
            year: int = None,
            licence: str = None) -> None:
        """
        Initialize Copyright instance.

        Args:
            author (str, optional): Author. Defaults to None.
            year (int, optional): Year. Defaults to None.
            licence (str, optional): Licence. Defaults to None.
        """
        self.author: str = author
        self.year: int = year
        self.licence: str = licence
        