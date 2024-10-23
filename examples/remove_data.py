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
