import ezgpx

# Check GPX schema when parsing file
gpx = ezgpx.GPX("file.gpx", check_xml_schemas=True, extensions_schemas=False)

# Check GPX schema and extensions schemas from GPX instance
gpx.check_xml_schemas(extensions_schemas=True)

# Check if written file follow GPX schema
gpx.to_gpx("new_file.gpx", check_xml_schemas=True, extensions_schemas=False)