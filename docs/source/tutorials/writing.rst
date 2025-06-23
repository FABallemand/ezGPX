Converting and Saving
---------------------

Converting to Dataframe
^^^^^^^^^^^^^^^^^^^^^^^

The :py:meth:`~to_pandas` method allows to convert a :py:class:`~ezgpx.gpx.GPX` object to a `Pandas Dataframe <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_.

.. code-block:: python

    from ezgpx import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")

    # Do stuff with GPX object

    # Convert to Pandas Dataframe
    df = gpx.to_pandas(values=["lat", "lon", "ele"])

The :py:meth:`~to_polars` method allows to convert a :py:class:`~ezgpx.gpx.GPX` object to a `Polars Dataframe <https://docs.pola.rs/api/python/stable/reference/dataframe/index.html>`_.

.. code-block:: python

    from ezgpx import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")

    # Do stuff with GPX object

    # Convert to Pandas Dataframe
    df = gpx.to_polars(values=["lat", "lon", "ele"])

Saving as GPX File
^^^^^^^^^^^^^^^^^^

The :py:meth:`~to_gpx` method allows to export a :py:class:`~ezgpx.gpx.GPX` object as a `GPX <https://en.wikipedia.org/wiki/GPS_Exchange_Format>`_ file.

.. code-block:: python

    from ezgpx import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")

    # Do stuff with GPX object

    # Save as GPX file
    gpx.to_gpx("new_file.gpx")

Saving as KML File
^^^^^^^^^^^^^^^^^^

The :py:meth:`~to_kml` method allows to export a :py:class:`~ezgpx.gpx.GPX` object as a `KML <https://en.wikipedia.org/wiki/Keyhole_Markup_Language>`_ file.

.. code-block:: python

    from ezgpx import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")

    # Do stuff with GPX object

    # Save as KML file
    gpx.to_kml("new_file.kml")

Saving as CSV File
^^^^^^^^^^^^^^^^^^

The :py:meth:`~to_csv` method allows to export a :py:class:`~ezgpx.gpx.GPX` object as a `CSV <https://en.wikipedia.org/wiki/Comma-separated_values>`_ file.

.. code-block:: python

    from ezgpx import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")

    # Do stuff with GPX object

    # Save as CSV file
    gpx.to_csv("new_file.csv", values=["lat", "lon", "ele"])
