

class GpxElement():
    """
    Base class for element in GPX file.
    Implements dunders functions.
    """

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        s = "("
        for a in self.mandatory_fields:
            s += f"{getattr(self, a)}, "
        s = s[:-2] + ")"
        return s

    def __repr__(self) -> str:
        s = f"{self.__class__.__name__}[{self.tag}]("
        for a in self.mandatory_fields:
            s += f"{getattr(self, a)}, "
        s = s[:-2] + ")"
        return s
