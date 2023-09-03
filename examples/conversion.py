import ezgpx

# Parse GPX file
gpx = ezgpx.GPX("file.gpx")

# Convert to Pandas Dataframe
df = gpx.to_dataframe()

# Convert to CSV
gpx.to_csv("file.csv", columns=["lat", "lon", "ele"])

# Convert to KML
gpx.to_kml("file.kml")