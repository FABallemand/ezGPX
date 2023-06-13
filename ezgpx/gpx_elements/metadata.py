

class Metadata():
    """
    Metadata (metadata) element in GPX file.
    """

    def __init__(self, link: str = "", link_text: str = "", time: str = ""):
        self.link = link
        self.link_text = link_text
        self.time = time