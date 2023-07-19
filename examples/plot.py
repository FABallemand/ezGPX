import ezgpx

# Parse GPX file
gpx = ezgpx.GPX("file.gpx")

# Plot with Matplotlib
gpx.matplotlib_plot(elevation_color=True,
                    start_stop_colors=("green", "red"),
                    way_points_color="blue",
                    title=gpx.name(),
                    duration=(0, 0),
                    distance=(0.5, 0),
                    ascent=None,
                    pace=(1, 0),
                    speed=None,
                    file_path="img_1")

# Plot with Matplotlib Basemap Toolkit
gpx.matplotlib_basemap_plot(base_color="darkorange",
                            start_stop_colors=("darkgreen", "darkred"),
                            way_points_color="darkblue",
                            title=gpx.name(),
                            duration=(0,0),
                            distance=(0.5,0),
                            ascent=None,
                            pace=None,
                            speed=(1,0),
                            file_path="img_2")

# Plot with gmplot (Google Maps)
gpx.gmplot_plot(base_color="yellow",
              start_stop_colors=("green", "red"),
              way_points_color="blue",
              zoom=14,
              title=gpx.name(),
              file_path="map_1.html",
              open=False)

# Plot with Folium
gpx.folium_plot(tiles="OpenStreetMap",
                base_color="orange",
                start_stop_colors=("green", "red"),
                way_points_color="blue",
                minimap=True,
                coord_popup=False,
                title="Very nice track!",
                zoom=8,
                file_path="map_2.html",
                open=True)

# Write new GPX file
gpx.to_gpx("new_file.gpx")
