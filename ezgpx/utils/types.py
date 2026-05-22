"""
This module contains utility functions for ezGPX types.
"""

import re
from datetime import datetime

from ezgpx.complex_types import (
    Bounds,
    Copyright,
    Email,
    Extensions,
    Gpx,
    Link,
    Metadata,
    Person,
    Pt,
    Ptseg,
    Rte,
    Trk,
    Trkseg,
    Wpt,
)
from ezgpx.simple_types import Degrees, DgpsStation, Fix, Latitude, Longitude

_ezGPXSimpleType = Degrees | DgpsStation | Fix | Latitude | Longitude
_ezGPXComplexType = (
    Bounds
    | Copyright
    | Email
    | Extensions
    | Gpx
    | Link
    | Metadata
    | Person
    | Pt
    | Ptseg
    | Rte
    | Trk
    | Trkseg
    | Wpt
)
_ezGPXType = _ezGPXSimpleType | _ezGPXComplexType


def split_attributes(s: str) -> list[str]:
    """
    Split attributes from string representation.

    Args:
        s (str): String representation of attributes.

    Returns:
        list[str]: List of string representations of attributes.

    Example:
    >>> metadata = Metadata(
    >>>     "test-name",
    >>>     "test-desc",
    >>>     Person(),
    >>>     Copyright("test-author"),
    >>>     [
    >>>         Link("test-href-0"),
    >>>         Link("test-href-1"),
    >>>     ],
    >>>     datetime(2000, 1, 1),
    >>>     "test_keywords",
    >>>     Bounds(0, 0, 0, 0),
    >>>     Extensions(),
    >>> )
    >>> split_attributes(str(metadata)[9:-1])
    ["name='test-name'",
    "desc='test-desc'",
    "author=Person(name=None, email=None, link=None, tag='author')",
    "copyright=Copyright(author='test-author', year=None, license=None, tag='copyright')",
    "link=[Link(href='test-href-0', text=None, type=None, tag='link'), Link(href='test-href-1', text=None, type=None, tag='link')]",
    'time=datetime.datetime(2000, 1, 1, 0, 0)',
    "keywords='test_keywords'",
    "bounds=Bounds(minlat=Latitude(value=0.0), minlon=Longitude(value=0.0), maxlat=Latitude(value=0.0), maxlon=Longitude(value=0.0), tag='bounds')",
    "extensions=Extensions(values=None, tag='extensions')",
    "tag='metadata'"]
    """
    parts = []
    current = []
    depth = 0

    for ch in s:
        if ch == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            if ch in ["(", "["]:
                depth += 1
            elif ch in [")", "]"]:
                depth -= 1
            current.append(ch)

    parts.append("".join(current).strip())
    return parts


def instance_from_str(s: str) -> _ezGPXType:
    """
    Create instance of ezGPX type from its string representation.

    Args:
        s (str): String representation of a ezGPX object.

    Raises:
        ValueError: Unable to parse attribute.

    Returns:
        _ezGPXType: Object matching the string representation.
    """
    m = re.match(r"^(\w+)\((.*)\)$", s)  # Match class name and attributes
    attr = []
    print(split_attributes(m.group(2)))
    for a in split_attributes(m.group(2)):
        v = a.split("=", maxsplit=1)[1]
        if v == "None":
            attr.append(None)
        elif v[0] == "'" and v[-1] == "'":
            attr.append(v[1:-1])
        elif v[0] == "[" and v[-1] == "]":
            attr.append(list(map(instance_from_str, split_attributes(v[1:-1]))))
        elif v.startswith("datetime.datetime"):
            attr.append(
                datetime(
                    *list(
                        map(
                            int,
                            re.search(
                                r"\((.*?)\)", "datetime.datetime(2000, 1, 1, 0, 0)"
                            )
                            .group(1)
                            .split(", "),
                        )
                    )
                )
            )
        elif bool(re.match(r"^(\w+)\((.*)\)$", v)):
            attr.append(instance_from_str(v))  # Recursive call for nested types
        else:
            try:
                attr.append(float(v))
            except (TypeError, ValueError) as e:
                raise ValueError("Unable to parse attribute.") from e
    return getattr(__import__("ezgpx"), m.group(1))(*attr)
