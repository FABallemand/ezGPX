"""
This module contains utility functions.
"""

from typing import Any

import narwhals as nw


def is_dataframe(obj: Any) -> bool:
    """
    Check if an object is a dataframe.
    """
    try:
        nw.from_native(obj)
        return True
    except Exception:  # pylint: disable=broad-exception-caught
        return False
