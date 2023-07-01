
class Bounds():
    """
    Bounds (bounds) element in GPX file.
    """

    def __init__(
            self,
            minlat: float = None,
            minlon: float = None,
            maxlat: float = None,
            maxlon: float = None) -> None:
        """
        Initialize Bounds instance.

        Args:
            minlat (float, optional): Minimal latitude. Defaults to None.
            minlon (float, optional): Minimal longitude. Defaults to None.
            maxlat (float, optional): Maximal latitude. Defaults to None.
            maxlon (float, optional): Maximal longitude. Defaults to None.
        """
        self.minlat: float = minlat
        self.minlon: float = minlon
        self.maxlat: float = maxlat
        self.maxlon: float = maxlon