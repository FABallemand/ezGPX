# 🗺️ ezGPX

![GitHub](https://img.shields.io/github/license/FABallemand/ezGPX)
![PyPI - Version](https://img.shields.io/pypi/v/ezgpx)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ezgpx)
![GitHub repo size](https://img.shields.io/github/repo-size/FABallemand/ezGPX)

![GitHub last commit](https://img.shields.io/github/last-commit/FABallemand/ezGPX/main)
![CI](https://github.com/FABallemand/ezGPX/actions/workflows/ci.yml/badge.svg?event=push)
[![Documentation Status](https://readthedocs.org/projects/ezgpx/badge/?version=latest)](https://ezgpx.readthedocs.io/en/latest/?badge=latest)

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
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
