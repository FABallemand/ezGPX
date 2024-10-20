Parsing
-------

GPX Files
^^^^^^^^^

In order to parse a GPX file, simply create a new :py:class:`~ezgpx.gpx.GPX` object with the path to the file.

.. note:: In the next tutorials you will learn how to plot, modify and save this :py:class:`~ezgpx.gpx.GPX` object to a file.

::

    import ezgpx

    # Parse GPX file
    gpx = ezgpx.GPX("file.gpx")


KML Files
^^^^^^^^^

In order to parse a KML file, simply create a new :py:class:`~ezgpx.gpx.GPX` object with the path to the file.

.. note:: This method is mainly designed to perform a simple conversion from KML to GPX. To that extent, only GPS data from the KML files will be processed.

::

    import ezgpx

    # Parse KML file
    gpx = ezgpx.GPX("file.kml")


KMZ Files
^^^^^^^^^

KML files are commonly distributed as KMZ files, which are zipped KML files with a .kmz extension.
In order to parse a KMZ file, simply create a new :py:class:`~ezgpx.gpx.GPX` object with the path to the file.

.. note:: This method will create a temporary KML file in the working directory.

.. note:: This method is mainly designed to perform a simple conversion from KMZ to GPX. To that extent, only GPS data from the one of the KML files found in the KMZ will be processed.

::

    import ezgpx

    # Parse KMZ file
    gpx = ezgpx.GPX("file.kmz")


FIT Files
^^^^^^^^^

In order to parse a FIT file, simply create a new :py:class:`~ezgpx.gpx.GPX` object with the path to the file.

::

    import ezgpx

    # Parse FIT file
    gpx = ezgpx.GPX("file.fit")