
class Bounds():
    """
    boundsType element in GPX file.
    """
    fields = ["minlat", "minlon", "maxlat", "maxlon"]
    mandatory_fields = []

    def __init__(
            self,
            tag: str = "bounds",
            minlat: float = None,
            minlon: float = None,
            maxlat: float = None,
            maxlon: float = None) -> None:
        """
        Initialize Bounds instance.

        Parameters
        ----------
        tag : str, optional
            XML tag, by default "bounds"
        minlat : float, optional
            Minimal latitude, by default None
        minlon : float, optional
            Minimal longitude, by default None
        maxlat : float, optional
            Maximal latitude, by default None
        maxlon : float, optional
            Maximal longitude, by default None
        """
        self.tag: str = tag
        self.minlat: float = minlat
        self.minlon: float = minlon
        self.maxlat: float = maxlat
        self.maxlon: float = maxlon