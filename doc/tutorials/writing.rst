Converting and Saving
---------------------

Save as GPX file
^^^^^^^^^^^^^^^^

The :py:meth:`~to_gpx` allows to export a :py:class:`~ezgpx.gpx.GPX` object as a `GPX <https://en.wikipedia.org/wiki/GPS_Exchange_Format>`_ file.

::

    from ezgpx import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")

    # Do stuff with GPX object

    # Save as GPX file
    gpx.to_gpx("new_file.gpx")

Save as KML file
^^^^^^^^^^^^^^^^

The :py:meth:`~to_kml` allows to export a :py:class:`~ezgpx.gpx.GPX` object as a `KML <https://en.wikipedia.org/wiki/Keyhole_Markup_Language>`_ file.

::

    from ezgpx import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")

    # Do stuff with GPX object

    # Save as KML file
    gpx.to_kml("new_file.kml")

Save as CSV file
^^^^^^^^^^^^^^^^

The :py:meth:`~to_csv` allows to export a :py:class:`~ezgpx.gpx.GPX` object as a `CSV <https://en.wikipedia.org/wiki/Comma-separated_values>`_ file.

::

    from ezgpx import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")

    # Do stuff with GPX object

    # Save as CSV file
    gpx.to_csv("new_file.csv", columns=["lat", "lon", "ele"])

Convert to Pandas Dataframe
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :py:meth:`~to_kml` allows to convert a :py:class:`~ezgpx.gpx.GPX` object as a `Pandas Dataframe <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_.

::

    from ezgpx import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")

    # Do stuff with GPX object

    # Convert to Pandas Dataframe
    df = gpx.to_dataframe()