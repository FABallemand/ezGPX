Analysing
---------

ezGPX provides many insights about the GPS contained in the file.

Name
^^^^

The name of the activity is easily accessible and editable using the :py:meth:`~name` and :py:meth:`~set_name` methods.

.. code-block:: python

    from ezgpx import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")

    # Print name
    print(gpx.name())

    # Change name
    gpx.set_name("New name")

Points
^^^^^^

ezGPX provides access to information related to points and their coordinates such as:

- The number of points
- The bounds (ie: minimum and maximum latitude and longitude)
- The coordinates of the center
- The first and last point
- The extreme points (ie: the points at which minimum and maximum latitude and longitude are reached)

.. code-block:: python

    from ezgpx import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")

    # Compute number of points
    nb_pts = gpx.nb_points()

    # Compute bounds
    min_lat, min_lon, max_lat, max_lon = gpx.bounds()

    # Compute center
    center_lat, center_lon = gpx.center()

    # Retrieve first/last point
    first_pt = gpx.first_point()
    last_pt = gpx.last_point()

    # Retrieve extreme points
    min_lat_pt, min_lon_pt, max_lat_pt, max_lon_pt = gpx.extreme_points()

Distance and Elevation
^^^^^^^^^^^^^^^^^^^^^^

There are several methods to compute insights related to distance and elevation. The total distance of the track is easily accessible using the :py:meth:`~distance` method. The other methods related to ascent and descent (rates) requires the :py:class:`~ezgpx.gpx.GPX` to contain elevation data.

.. note:: Distances are expressed in metres (m) and rates in percentage (%).

.. code-block:: python

    from ezgpx import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")

    # Compute distance
    dist = gpx.distance()

    # Compute ascent
    ascent = gpx.ascent()

    # Compute descent
    descent = gpx.descent()

    # Compute minimum/maximum altitude
    min_ele = gpx.min_elevation()
    max_ele = gpx.max_elevation()

    # Compute ascent rate at each point
    # Note: this function is executed by all methods that require
    # ascent rate of points
    gpx.compute_points_ascent_rate()

    # Compute minimum/maximum ascent rate
    min_ascent_rate = gpx.min_ascent_rate()
    max_ascent_rate = gpx.max_ascent_rate()

Time
^^^^

If a :py:class:`~ezgpx.gpx.GPX` object contains time related data (mainly time-stamp at each point), many useful informations can be accessed.

.. code-block:: python

    from ezgpx import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")

    # Retrieve start/stop time
    start_time = gpx.start_time()
    stop_time = gpx.stop_time()

    # Compute the total amount of time elapsed
    elapsed_time = gpx.total_elapsed_time()

    # Compute the total amount of time stopped
    elapsed_time = gpx.stopped_time()

    # Compute the total amount of time spent moving
    elapsed_time = gpx.moving_time()

Speed and Pace
^^^^^^^^^^^^^^

If a :py:class:`~ezgpx.gpx.GPX` object contains time related data (mainly time-stamp at each point), it is possible to gain speed and pace insights. Furthermore, if elevation data are also available, ascent speeds can be computed!

.. note:: Speeds are expressed in kilometres per hour (km/h) and paces in minutes per kilometre (min/km).

.. code-block:: python

    from ezgpx import GPX

    # Parse GPX file
    gpx = GPX("file.gpx")

    # Compute average speed
    avg_speed = gpx.avg_speed()

    # Compute average speed while moving
    avg_speed = gpx.avg_moving_speed()

    # Compute speed at each point
    # Note: this function is executed by all methods that require
    # speed at each point
    gpx.compute_points_speed()

    # Retrieve minimum/maximum speed reached at a point
    min_speed = gpx.min_speed()
    max_speed = gpx.max_speed()

    # Compute average pace
    avg_pace = gpx.avg_pace()

    # Compute average pace while moving
    avg_pace = gpx.avg_moving_pace()

    # Compute pace at each point
    # Note: this function is executed by all methods that require
    # pace at each point
    gpx.compute_points_pace()

    # Retrieve minimum/maximum pace reached at a point
    min_pace = gpx.min_pace()
    max_pace = gpx.max_pace()

    # Compute ascent_speed at each point
    # Note: this function is executed by all methods that require
    # ascent speed at each point
    gpx.compute_points_ascent_speed()

    # Retrieve minimum/maximum ascent speed reached at a point
    min_ascent_speed = gpx.min_ascent_speed()
    max_ascent_speed = gpx.max_ascent_speed()