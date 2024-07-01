
class Copyright():
    """
    copyrightType element in GPX file.
    """
    fields = ["author", "year", "licence"]
    mandatory_fields = ["author"]

    def __init__(
            self,
            tag: str = "copyright",
            author: str = None,
            year: int = None,
            licence: str = None) -> None:
        """
        Initialize Copyright instance.

        Parameters
        ----------
        tag : str, optional
            XML tag, by default "copyright"
        author : str, optional
            Author, by default None
        year : int, optional
            Year, by default None
        licence : str, optional
            Licence, by default None
        """
        self.tag: str = tag
        self.author: str = author
        self.year: int = year
        self.licence: str = licence
        