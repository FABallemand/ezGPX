"""
This module contains the Gpx class.
"""

from dataclasses import dataclass
from typing import ClassVar

from .extensions import Extensions
from .metadata import Metadata
from .rte import Rte
from .trk import Trk
from .wpt import Wpt


@dataclass
class Gpx:  # pylint: disable=too-many-instance-attributes
    """
    gpxType: GPX documents contain a metadata header, followed by
    waypoints, routes, and tracks. You can add your own elements to the
    extensions section of the GPX document.

    Args:

        version (str): Version number. Defaults to "1.1".
        creator (str): Name or URL of the software that created your
            GPX document. This allows others to inform the creator of a
            GPX instance document that fails to validate.
            Defaults to "ezGPX".
        metadata (Metadata, optional): Metadata about the file.
            Defaults to None.
        wpt (list[Wpt], optional): A list of waypoints.
            Defaults to None.
        rte (list[Rte], optional): A list of routes.
            Defaults to None.
        trk (list[Trk], optional): A list of tracks.
            Defaults to None.
        extensions (Extensions, optional): You can add extend GPX by
            adding your own elements from another schema here.
            Defaults to None.
        tag (str, optional): XML tag. Defaults to "gpx".
    """

    version: str
    creator: str
    metadata: Metadata = None
    wpt: list[Wpt] = None
    rte: list[Rte] = None
    trk: list[Trk] = None
    extensions: Extensions = None
    tag: str = "gpx"

    _fields: ClassVar[list[str]] = [
        "version",
        "creator",
        "metadata",
        "wpt",
        "rte",
        "trk",
        "extensions",
    ]
    _mandatory_fields: ClassVar[list[str]] = ["version", "creator"]

    def __post_init__(self):
        if not isinstance(self.version, str):
            self.version = str(self.version)
        if not isinstance(self.creator, str):
            self.creator = str(self.creator)
        if self.metadata is not None and not isinstance(self.metadata, Metadata):
            raise TypeError("`metadata` must be of type Metadata")
        if self.wpt is not None and (
            not isinstance(self.wpt, list)
            or not all(isinstance(w, Wpt) for w in self.wpt)
        ):
            raise TypeError("`wpt` must be of type list[Wpt]")
        if self.rte is not None and (
            not isinstance(self.rte, list)
            or not all(isinstance(r, Rte) for r in self.rte)
        ):
            raise TypeError("`rte` must be of type list[Rte]")
        if self.trk is not None and (
            not isinstance(self.trk, list)
            or not all(isinstance(t, Trk) for t in self.trk)
        ):
            raise TypeError("`trk` must be of type list[Trk]")
        if self.extensions is not None and not isinstance(self.extensions, Extensions):
            raise TypeError("`extensions` must be of type Extensions")
        if not isinstance(self.tag, str):
            self.tag = str(self.tag)
