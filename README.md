# 🗺️ ezGPX

![GitHub](https://img.shields.io/github/license/FABallemand/ezGPX)
![PyPI - Version](https://img.shields.io/pypi/v/ezgpx)
![GitHub last commit](https://img.shields.io/github/last-commit/FABallemand/ezGPX/main)
![CI](https://github.com/FABallemand/ezGPX/actions/workflows/ci.yml/badge.svg?event=push)
[![Documentation Status](https://readthedocs.org/projects/ezgpx/badge/?version=latest)](https://ezgpx.readthedocs.io/en/latest/?badge=latest)
![GitHub repo size](https://img.shields.io/github/repo-size/FABallemand/ezGPX)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ezgpx)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


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

# Write new simplified GPX file
gpx.to_gpx("new_file.gpx")
```

## 👤 Author
- Fabien ALLEMAND
