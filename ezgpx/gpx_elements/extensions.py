
class Extensions():
    """
    extensionsType element in GPX file.
    """
    fields = []
    mandatory_fields = []

    def __init__(
            self,
            tag: str = "extensions",
            values: dict = {}):
        self.tag: str = tag
        self.values: dict = values
