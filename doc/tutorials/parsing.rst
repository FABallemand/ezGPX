Parsing
-------

In order to parse a GPX file, simply create a new :py:class:`~ezgpx.gpx.GPX` object with the path to the file.

.. note::

    In the next tutorials you will learn how to plot, modify and save this :py:class:`~ezgpx.gpx.GPX` object.

::

    from ezGPX import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")