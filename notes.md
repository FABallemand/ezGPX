## 📚 References:

### 🖥️ Implementation

#### 💾 Python XML Parsing:
- Real Python: [A roadmap to XML Parsers in Python](https://realpython.com/python-xml-parser/#learn-about-xml-parsers-in-pythons-standard-library)
- [xml.etree.ElementTree — The ElementTree XML API](https://docs.python.org/3/library/xml.etree.elementtree.html)
- GeeksForGeeks: [Reading and Writing XML Files in Python](https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/)

#### 🌏 Map Projection
- Wikipedia: [Web Mercator projection](https://en.wikipedia.org/wiki/Web_Mercator_projection)

#### 🗃️ Creating a Python Library
- Medium: [How to create a Python library](https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f)
- Towards Data Science: [Deep dive: Create and publish your first Python library](https://towardsdatascience.com/deep-dive-create-and-publish-your-first-python-library-f7f618719e14)

### 🧭 Other Python GPX Library
- [gpxpy](https://github.com/tkrajina/gpxpy)

## 📝 TO DO LIST !!
- Complete gpx
```xml
<gpx
version="1.1 [1] ?"
creator="xsd:string [1] ?">
<metadata> metadataType </metadata> [0..1] ?
<wpt> wptType </wpt> [0..*] ?
<rte> rteType </rte> [0..*] ?
<trk> trkType </trk> [0..*] ?
<extensions> extensionsType </extensions> [0..1] ?
</gpx>
```
- Garmin extensions
- Compute length properly
- Unify topo types (ex: trkpt is a subclass of wpt) ie: add tags in class, parser, writer