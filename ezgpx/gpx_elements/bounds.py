
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
        self.minlat: float = minlat
        self.minlon: float = minlon
        self.maxlat: float = maxlat
        self.maxlon: float = maxlon