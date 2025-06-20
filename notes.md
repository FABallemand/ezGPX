# 📚 References:

## 🖥️ Implementation

### 💾 File Formats

#### 🏷️ XML
- [GPX XML Schema](http://www.topografix.com/GPX/1/1/)
- [KML XML Schema](http://schemas.opengis.net/kml/2.2.0/ogckml22.xsd)
- Real Python: [A roadmap to XML Parsers in Python](https://realpython.com/python-xml-parser/#learn-about-xml-parsers-in-pythons-standard-library)
- [xml.etree.ElementTree — The ElementTree XML API](https://docs.python.org/3/library/xml.etree.elementtree.html)
- GeeksForGeeks: [Reading and Writing XML Files in Python](https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/)
- [Validating XML with Python: A Step-by-Step Guide](https://medium.com/@murungaephantus/validating-xml-with-python-a-step-by-step-guide-53d4a4b9716b) (Does not work...)
- [xmlschema](https://xmlschema.readthedocs.io/en/latest/usage.html)

#### 🌐 GPX

#### 🇬 KML & KMZ

#### ⌚ FIT
- Garmin: [Flexible and Interoperable Data Transfer (FIT) Protocol](https://developer.garmin.com/fit/protocol/)

## 🌏 Map Plotting

### 🖥️ APIs

###
- [gmplot](https://github.com/gmplot/gmplot)
###
- [Basemap Matplotlib Toolkit](https://matplotlib.org/basemap/index.html)
- [Basemap tutorial](https://basemaptutorial.readthedocs.io/en/latest/index.html)
###
- Pypi: [folium](https://pypi.org/project/folium/)
- [Folium Quickstart](https://python-visualization.github.io/folium/quickstart.html#Polylines)
###
- [OSMPythonTools](https://wiki.openstreetmap.org/wiki/OSMPythonTools)
- Towards Data Science: [Loading Data from OpenStreetMap with Python and the Overpass API](https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0)

### 🗺️ Projections
- Wikipedia: [Web Mercator projection](https://en.wikipedia.org/wiki/Web_Mercator_projection)

### 📏 Units
- GPS Forums: [Explanation sought concerning gps semicircles](https://www.gps-forums.com/threads/explanation-sought-concerning-gps-semicircles.1072/)

## 🗃️ Creating a Python Library
- Medium: [How to create a Python library](https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f)
- Towards Data Science: [Deep dive: Create and publish your first Python library](https://towardsdatascience.com/deep-dive-create-and-publish-your-first-python-library-f7f618719e14)

## 🧭 Other Python GPX Library
- [gpxpy](https://github.com/tkrajina/gpxpy)
- [PyGPX](https://github.com/sgraaf/gpx)
- [gpxcsv](https://github.com/astrowonk/gpxcsv)

# 📝 TO DO LIST !!
- Save plotly plots as json
- Add str and repr methods to all class
- Merge method
- Compute length properly (improve haversine distance precision, 2D, 3D)
- Tests
- Update docstring (Google style + content [description from xsd])
- Normalize class names and attributes with GPX names
- Add units to docstrings
- Add meridian plot with basemap
- Add support for all emojis in plots
- Handle errors properly and remove logging
- Add descent rate?
- Improve time computation for pauses?
- Add descent speed?
- Add polars to dict methods ??? (https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.to_dict.html, https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.rows_by_key.html#polars.DataFrame.rows_by_key, https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.to_dicts.html#polars.DataFrame.to_dicts)
