Writing
-------

Save as GPX file
^^^^^^^^^^^^^^^^

The :py:meth:`~to_gpx` allows to export a :py:class:`~ezgpx.gpx.GPX` object as a GPX file.

::

    from ezgpx import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")

    # Do stuff with GPX object

    # Save as GPX file
    gpx.to_gpx("new_file.gpx")