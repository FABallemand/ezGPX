# 🗺️ ezGPX

![GitHub](https://img.shields.io/github/license/FABallemand/ezGPX)
![PyPI - Version](https://img.shields.io/pypi/v/ezgpx)
![GitHub last commit](https://img.shields.io/github/last-commit/FABallemand/ezGPX/main)
![CI](https://github.com/FABallemand/ezGPX/actions/workflows/ci.yml/badge.svg?event=push)
[![Documentation Status](https://readthedocs.org/projects/ezgpx/badge/?version=latest)](https://ezgpx.readthedocs.io/en/latest/?badge=latest)
![GitHub repo size](https://img.shields.io/github/repo-size/FABallemand/ezGPX)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ezgpx)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

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

# Plot using matplotlib
# See documentation and examples for more plotting methods!
plotter = ezgpx.MatplotlibPlotter(gpx)
plotter.plot(
    figsize=(16, 9),
    size=50,
    color="ele",
    cmap=matplotlib.cm.get_cmap("viridis", 12),
    colorbar=True,
    start_point_color="green",
    stop_point_color="red",
    way_points_color="blue",
    background="World_Imagery",
    title=gpx.name(),
    title_fontsize=30,
    file_path="matplotlib.png"
)

# Simplify (using Ramer-Dougle-Peucker algorithm)
gpx.simplify()

# Remove metadata
gpx.remove_metadata()

# Write new simplified GPX file
gpx.to_gpx("new_file.gpx")
```

![Plot made with Matplotlib](img/matplotlib.png)

## 👤 Author
- Fabien ALLEMAND
