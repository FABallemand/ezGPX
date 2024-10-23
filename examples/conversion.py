import ezgpx

# Parse GPX file
gpx = ezgpx.GPX("file.gpx")

# Save as GPX file
gpx.to_gpx("new_file.gpx")

# Save as KML file
gpx.to_kml("new_file.kml")

# Save as CSV file
gpx.to_csv("new_file.csv", values=["lat", "lon", "ele"])

# Convert to Pandas Dataframe
df = gpx.to_dataframe()
