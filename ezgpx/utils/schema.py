"""
This module contains functions to validate XML files against XML schemas.
"""

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

import warnings
from pathlib import Path
from typing import Optional

import xmlschema


def check_xml_schema(file_path: str | Path, version: Optional[str] = None) -> bool:
    """
    Check XML schema.

    Parameters
    ----------
    file_path : str
        File path

    Returns
    -------
    bool
        True if the file follows XML schemas
    """
    file_path = Path(file_path)
    schema = None

    # GPX
    if file_path.suffix == ".gpx":
        if version is None or version == "1.1":
            schema = xmlschema.XMLSchema(
                files("ezgpx.schemas").joinpath("gpx_1_1/gpx.xsd")
            )
        elif version == "1.0":
            schema = xmlschema.XMLSchema(
                files("ezgpx.schemas").joinpath("gpx_1_0/gpx.xsd")
            )
        else:
            warnings.warn("Unable to check XML schema (unsupported GPX version)")
            return False

    # KML
    elif file_path.suffix == ".kml":
        schema = xmlschema.XMLSchema(
            files("ezgpx.schemas").joinpath("kml_2_2/ogckml22.xsd")
        )

    # KMZ
    elif file_path.suffix == ".kmz":
        return False

    # FIT
    elif file_path.suffix == ".fit":
        warnings.warn("Unable to check XML schema (fit files are not XML files)")
        return False

    # NOT SUPPORTED
    else:
        warnings.warn("Unable to check XML schema (unable to identify file type)")
        return False

    if schema is not None:
        return schema.is_valid(file_path)
    warnings.warn("Unable to check XML schema (unable to load XML schema)")
    return False


def check_xml_extensions_schemas(file_path: str | Path) -> bool:
    """
    Check XML extensions schemas.

    Parameters
    ----------
    file_path : str
        Path to GPX file.

    Returns
    -------
    bool
        True if GPX file follows XML extensions schemas.
    """
    raise NotImplementedError(
        "XML extensions schema validation is not implemented yet."
    )
    # gpx_schemas = [s for s in self.xsi_schema_location if s.endswith(".xsd")]
    # gpx_schemas.remove("http://www.topografix.com/GPX/1/1/gpx.xsd")
    # for gpx_schema in gpx_schemas:
    #     schema = xmlschema.XMLSchema(gpx_schema)
    #     if not schema.is_valid(file_path):
    #         warnings.warn(f"File does not follow {gpx_schema}")
    #         return False
    # return True
