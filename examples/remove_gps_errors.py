from ezgpx import GPX

# Parse GPX file
gpx = GPX("file.gpx")

# Remove GPS errors
gpx.remove_gps_errors()

# Write new simplified GPX file
gpx.to_gpx("new_file.gpx")