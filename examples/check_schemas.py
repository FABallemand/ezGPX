import ezgpx

# Check GPX schema when parsing file
gpx = ezgpx.GPX("file.gpx", xml_schema=True, xml_extensions_schemas=False)

# Check GPX schema from GPX instance
gpx.check_xml_schema()

# Check extensions schemas from GPX instance
gpx.check_xml_extensions_schemas()

# Check if written file follow GPX schema
gpx.to_gpx("new_file.gpx", xml_schema=True, xml_extensions_schemas=False)
