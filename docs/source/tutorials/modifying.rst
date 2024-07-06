Modifying
---------

Remove Data
^^^^^^^^^^^

All data contained in a GPX file are not always relevant. By working with :py:class:`~ezgpx.gpx.GPX` objects, it is possible to remove useless data such as metadata, elevation and time data.

::

    from ezgpx import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")

    # Remove metadata
    gpx.remove_metadata()

    # Remove elevation data
    gpx.remove_elevation()

    # Remove time data
    gpx.remove_time()

    # Write new simplified GPX file
    gpx.to_gpx("new_file.gpx")

Remove GPS Errors
^^^^^^^^^^^^^^^^^

GPS devices sometimes loose signal generating errors in GPX files. The most noticeable errors (single isolated points) can be found and removed as follow.

::

    import ezgpx

    # Parse GPX file
    gpx = ezgpx.GPX("file.gpx")

    # Remove GPS errors
    gpx.remove_gps_errors()

    # Write new simplified GPX file
    gpx.to_gpx("new_file.gpx")

Simplify Track
^^^^^^^^^^^^^^

It is sometimes usefull to reduce the amount of track points contained in a GPX file especially when working with low power and low capacity GPS devices. The :py:meth:`~simplify` allows to reduce the number of points while keeping a great precision.

::

    import ezgpx

    # Parse GPX file
    gpx = ezgpx.GPX("file.gpx")

    # Simplify (using Ramer-Douglas-Peucker algorithm)
    gpx.simplify()

    # Write new simplified GPX file
    gpx.to_gpx("new_file.gpx")

In the following example, one manage to go from 3263 track points to only 1082. This correspond to a 69% decrease in points and allows to save 704.6 kB (ie: 85.4% of the original file size) by reducing the file size from 824.8 kB to 120.2 kB.

::

    from ezgpx import GPX

    # Load and parse GPX file
    gpx = GPX("file.gpx")

    # Print number of track points
    print(f"nb_points = {gpx.nb_points()}")

    # Plot tracks
    gpx.matplotlib_plot(start_stop_colors=("green", "red"), way_points_color="blue", elevation_color=True, title="Run", duration=(0,0), distance=(0.5,0), ascent=(1,0))

    # Simplify tracks
    gpx.simplify()

    # Print new number of track points
    print(f"nb_points = {gpx.nb_points()}")

    # Plot tracks
    gpx.matplotlib_plot(start_stop_colors=("green", "red"), way_points_color="blue", elevation_color=True, title="Run", duration=(0,0), distance=(0.5,0), ascent=(1,0))

    # Save GPX
    gpx.to_gpx("file_simplified.gpx")

.. image:: ../../../img/simplify_1.png
  :width: 500
  :alt: Track plot followed by the simplified track plot