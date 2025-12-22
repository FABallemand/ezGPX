from .gpx_element import GpxElement


class Extensions(GpxElement):
    """
    extensionsType element in GPX file.
    """

    fields = []
    mandatory_fields = []

    def __init__(self, tag: str = "extensions", values: dict = None):
        self.tag: str = tag
        self.values: dict = values if values is not None else {}
