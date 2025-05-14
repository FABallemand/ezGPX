# 🗺️ ezGPX

![GitHub](https://img.shields.io/github/license/FABallemand/ezGPX)
![PyPI - Version](https://img.shields.io/pypi/v/ezgpx)
![GitHub last commit](https://img.shields.io/github/last-commit/FABallemand/ezGPX/main)
[![Documentation Status](https://readthedocs.org/projects/ezgpx/badge/?version=latest)](https://ezgpx.readthedocs.io/en/latest/?badge=latest)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ezgpx)
<!-- ![CI](https://github.com/FABallemand/ezGPX/actions/workflows/ci.yml/badge.svg?event=push) -->

## 🔎 Description
ezGPX is an easy to use Python library for working with GPX files.

Read, modify, write, and extract insights from your activity data with ease!

- PyPi: https://pypi.org/project/ezgpx/
- Documentation: https://ezgpx.readthedocs.io/en/latest/
- Source code: https://github.com/FABallemand/ezGPX
- Bug reports: https://github.com/FABallemand/ezGPX/issues

## 🛠️ Installation

```bash
pip install ezgpx
```

## 🏁 Get started

```python
import ezgpx
import matplotlib

# Parse GPX file
gpx = ezgpx.GPX("file.gpx")

# Simplify (using Ramer-Dougle-Peucker algorithm)
gpx.simplify()

# Remove metadata
gpx.remove_metadata()

# Plot with Matplotlib
test_gpx.matplotlib_plot(figsize=(16,9),
                         size=6,
                         color="ele",
                         cmap=matplotlib.cm.get_cmap("gnuplot", 12),
                         colorbar=False,
                         start_point_color="green",
                         stop_point_color="red",
                         way_points_color=None,
                         background="World_Imagery",
                         offset_percentage=0.04,
                         dpi=100,
                         title=test_gpx.name(),
                         title_fontsize=20,
                         watermark=True,
                         file_path="img_1.png")

# Write new simplified GPX file
gpx.to_gpx("new_file.gpx")
```
![](img/matplotlib_plot_1.jpg)

## 🏋️ Advanced Use

```python
import ezgpx
import matplotlib

# Parse GPX file
gpx = ezgpx.GPX("file.gpx")

# Plot with Matplotlib
test_gpx.expert_plot(figsize=(16,9),
                     subplots=(3,2),
                     map_position=(0,0),
                     map_size=10,
                     map_color="ele",
                     map_cmap=matplotlib.cm.get_cmap("viridis", 12),
                     map_colorbar=True,
                     start_point_color=None,
                     stop_point_color=None,
                     way_points_color=None,
                     background="World_Imagery",
                     offset_percentage=0.04,
                     xpixels=1000,
                     ypixels=None,
                     dpi=100,
                     elevation_profile_position=(1,0),
                     elevation_profile_size=10,
                     elevation_profile_color="ele",
                     elevation_profile_cmap=matplotlib.cm.get_cmap("viridis", 12),
                     elevation_profile_colorbar=False,
                     elevation_profile_grid=True,
                     elevation_profile_fill_color="lightgray",
                     elevation_profile_fill_alpha=0.5,
                     pace_graph_position=(2,0),
                     pace_graph_size=10,
                     pace_graph_color="ele",
                     pace_graph_cmap=None,
                     pace_graph_colorbar=False,
                     pace_graph_grid=True,
                     pace_graph_fill_color="lightgray",
                     pace_graph_fill_alpha=0.5,
                     pace_graph_threshold=15,
                     ascent_rate_graph_position=(1,1),
                     made_with_ezgpx_position=(0,1),
                     shared_color="ele",
                     shared_cmap=None,
                     shared_colorbar=True,
                     data_table_position=(2,1),
                     title=test_gpx.name(),
                     title_fontsize=20,
                     watermark=False,
                     file_path="img_2.png")
```
![](img/expert_plot_1.jpg)

## 👤 Author
- Fabien ALLEMAND