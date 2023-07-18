import ezgpx

# Parse GPX file
gpx = ezgpx.GPX("file.gpx")

# Simplify (using Ramer-Douglas-Peucker algorithm)
gpx.simplify()

# Write new simplified GPX file
gpx.to_gpx("new_file.gpx")