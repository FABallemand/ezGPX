import matplotlib as mpl

import ezgpx

# Parse GPX file
gpx = ezgpx.GPX("file.gpx")

# Plot with Matplotlib
plotter = ezgpx.MatplotlibPlotter(gpx)
plotter.plot(
    figsize=(16, 9),
    size=50,
    color="ele",
    cmap=mpl.cm.get_cmap("viridis", 12),
    colorbar=True,
    start_point_color="green",
    stop_point_color="red",
    background="World_Imagery",
    title=gpx.name(),
    title_fontsize=30,
    file_path="matplotlib.png",
)

# Animated plot with Matplotlib
plotter = ezgpx.MatplotlibAnimPlotter(gpx)
plotter.plot(
    figsize=(16, 9),
    size=10,
    color="#FFA800",
    background="World_Imagery",
    dpi=50,
    fps=34,
    repeat=True,
    title="Trail Running",
    title_fontsize=30,
    file_path="matplotlib.gif",
)

# Plot with Plotly
plotter = ezgpx.PlotlyPlotter(gpx)
plotter.plot(
    tiles="open-street-map",
    mode="lines+markers",
    color="#FFA800",
    start_stop_colors=("green", "red"),
    way_points_color="blue",
    title=gpx.name(),
    zoom=12,
    file_path="plotly.html",
)

# Animated plot with Plotly
plotter = ezgpx.PlotlyAnimPlotter(gpx)
plotter.plot(
    tiles="open-street-map",
    color="#FFA800",
    title=gpx.name(),
    zoom=12,
    file_path="plotly.gif",
)

# Plot with gmplot (Google Maps)
plotter = ezgpx.GmplotPlotter(gpx)
plotter.plot(
    color="#FFA800",
    start_stop_colors=("green", "red"),
    way_points_color="blue",
    scatter=True,
    plot=False,
    zoom=15,
    file_path="gmap.html",
    browser=True,
)

# Plot with Folium
plotter = ezgpx.FoliumPlotter(gpx)
plotter.plot(
    tiles="OpenStreetMap",
    color="#FFA800",
    start_stop_colors=("green", "red"),
    way_points_color="blue",
    minimap=True,
    coord_popup=True,
    zoom=15,
    file_path="folium.html",
    browser=True,
)

##############################################################################

# Plot with Papermap
# See: https://pypi.org/project/papermap/0.2.2/

from papermap import PaperMap

# Create map
lat, lon = gpx.center()
pm = PaperMap(lat=lat, lon=lon)

# Render map
pm.render()

# Save map
pm.save("map.pdf")
