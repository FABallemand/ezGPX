Checking Schemas
----------------

There are tree ways to check if a GPX file follows the XML schemas.
In all cases, the GPX file will be checked for the relevant Topographix GPX schema (either version 1.0 or 1.1).
If the :py:param:`~extensions_schemas` is set to :py:const:`~True`, then the GPX file will be tested for all schemas that are listed.

During Parsing
^^^^^^^^^^^^^^

It is possible to check during parsing, in which case an invalid GPX file will raise an error.

::

    import ezgpx

    # Check GPX schema when parsing file
    gpx = ezgpx.GPX("file.gpx", check_schemas=True, extensions_schemas=False)

Test a :py:class:`~ezgpx.gpx.GPX` Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A :py:class:`~ezgpx.gpx.GPX` object can directly be checked.

::

    import ezgpx

    gpx = GPX("file.gpx", check_schemas=False)

    # Check GPX schema and extensions schemas from GPX instance
    gpx.check_schemas(extensions_schemas=True)

After Writting
^^^^^^^^^^^^^^

It is possible to check whether a written GPX file follows XML schemas.

::

    import ezgpx

    gpx = GPX("file.gpx", check_schemas=False)

    # Check if written file follow GPX schema
    if gpx.to_gpx("new_file.gpx", check_schemas=True, extensions_schemas=False) == False:
        print("new_file.gpx does not follow the GPX 1.1 schema!!")