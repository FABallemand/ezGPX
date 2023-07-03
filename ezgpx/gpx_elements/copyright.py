
class Copyright():
    """
    copyrightType element in GPX file.
    """

    def __init__(
            self,
            tag: str = "copyright",
            author: str = None,
            year: int = None,
            licence: str = None) -> None:
        """
        Initialize Copyright instance.

        Args:
            tag (str, optional): XML tag. Defaults to "copyright".
            author (str, optional): Author. Defaults to None.
            year (int, optional): Year. Defaults to None.
            licence (str, optional): Licence. Defaults to None.
        """
        self.tag: str = tag
        self.author: str = author
        self.year: int = year
        self.licence: str = licence
        