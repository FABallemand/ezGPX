from .gpx_element import GpxElement


class Link(GpxElement):
    """
    linkType element in GPX file.
    """
    fields = ["href", "text", "type"]
    mandatory_fields = ["href"]

    def __init__(
            self,
            tag: str = "link",
            href: str = None,
            text: str = None,
            type_: str = None) -> None:
        """
        Initialize Link instance.

        Parameters
        ----------
        tag : str, optional
            XML tag, by default "link"
        href : str, optional
            Hyper reference, by default None
        text : str, optional
            Text, by default None
        type : str, optional
            Type, by default None
        """
        self.tag: str = tag
        self.href: str = href
        self.text: str = text
        self.type: str = type_
