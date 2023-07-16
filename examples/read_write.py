import ezgpx

# Parse GPX file
gpx = ezgpx.GPX("file.gpx")

# Write new GPX file
gpx.to_gpx("new_file.gpx")