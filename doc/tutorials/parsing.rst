Parsing
-------

GPX Files
^^^^^^^^^

In order to parse a GPX file, simply create a new :py:class:`~ezgpx.gpx.GPX` object with the path to the file.

.. note::

    In the next tutorials you will learn how to plot, modify and save this :py:class:`~ezgpx.gpx.GPX` object.

::

    from ezGPX import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")


KML Files
^^^^^^^^^

In order to parse a KML file, simply create a new :py:class:`~ezgpx.gpx.GPX` object with the path to the file.

.. note::

    This method is mainly designed to perform a simple conversion from KML to GPX. To that extent, only GPS data from the KML files will be processed.

::

    from ezGPX import GPX

    # Parse KML file
    gpx = GPX("file.kml")