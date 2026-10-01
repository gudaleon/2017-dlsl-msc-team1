# 🌊 Watershed Analysis Dashboard

> **Interactive visualization and analysis of watershed boundaries from ArcGIS shapefiles**  
> Inspired by USGS SPARROW mappers

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.29+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-Open%20Source-green.svg)]()

Transform your ArcGIS watershed shapefiles into interactive, web-based visualizations with powerful analysis tools—no GIS software required!

## 🎯 What Is This?

This dashboard allows you to:
- 🗺️ **Visualize** watershed boundaries on interactive maps
- 📊 **Analyze** attribute data with automatic statistics and charts
- 🎨 **Color** watersheds by any numeric attribute (choropleth)
- 🔍 **Filter** and search through your data
- 📥 **Export** results to CSV
- 🚀 **Share** via web browser

**Perfect for:** Environmental scientists, watershed managers, GIS analysts, researchers, students, and anyone working with watershed data.

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Interactive Maps** | Multiple base layers, zoom, pan, measure tools |
| **Choropleth Mapping** | Color watersheds by attributes with 10+ color schemes |
| **Statistical Analysis** | Auto-generated summaries and distribution charts |
| **Data Filtering** | Filter by attribute ranges in real-time |
| **Search & Export** | Full-text search and CSV export |
| **Multiple Formats** | Streamlit and Dash implementations |
| **Docker Ready** | One-command deployment |
| **Sample Data** | Built-in generator for testing |

## 🚀 Quick Start

### 1. Install

```bash
pip install -r requirements.txt
```

### 2. Run

```bash
streamlit run watershed_dashboard.py
```

### 3. Load Data

Open `http://localhost:8501` and upload your shapefile components (.shp, .shx, .dbf, .prj)

### 4. Explore

Navigate through tabs: Map, Statistics, Data Table, Metadata

**That's it!** 🎉

## 📸 Screenshots

### Interactive Map View
```
┌────────────────────────────────────────────────────┐
│ Multiple base layers  │  Hover tooltips           │
│ Choropleth coloring   │  Measurement tools        │
│ Zoom/Pan controls     │  Fullscreen mode          │
└────────────────────────────────────────────────────┘
```

### Statistical Analysis
```
┌────────────────────────────────────────────────────┐
│ Summary statistics    │  Distribution histograms  │
│ Mean, median, std dev │  Pattern identification   │
│ Min/max ranges        │  Interactive charts       │
└────────────────────────────────────────────────────┘
```

### Data Table & Export
```
┌────────────────────────────────────────────────────┐
│ Searchable table      │  Sort by any column       │
│ Filter display        │  CSV export               │
│ All attributes shown  │  Excel-compatible         │
└────────────────────────────────────────────────────┘
```

## 📚 Documentation

| Document | Description | Time |
|----------|-------------|------|
| [QUICKSTART.md](QUICKSTART.md) | Get running in 5 minutes | ⏱️ 5 min |
| [VISUAL_GUIDE.md](VISUAL_GUIDE.md) | Step-by-step visual walkthrough | 📸 10 min |
| [WATERSHED_README.md](WATERSHED_README.md) | Complete documentation | 📖 30 min |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Technical overview | 🔧 15 min |
| [watershed_tutorial.ipynb](watershed_tutorial.ipynb) | Hands-on Jupyter tutorial | 💻 60 min |

**Start here:** [QUICKSTART.md](QUICKSTART.md) → [VISUAL_GUIDE.md](VISUAL_GUIDE.md)

## 🛠️ What's Included

### Dashboard Applications
- **`watershed_dashboard.py`** - Streamlit version (recommended)
- **`watershed_dashboard_dash.py`** - Dash version (alternative)
- **`config.py`** - Customization settings

### Utility Scripts
- **`shapefile_utils.py`** - Validate, clean, convert shapefiles
- **`create_sample_data.py`** - Generate test data

### Deployment
- **`Dockerfile`** - Container configuration
- **`docker-compose.yml`** - Multi-service setup
- **`requirements.txt`** - Dependencies

## 💡 Common Use Cases

### 🌍 Watershed Management
```
✓ Visualize watershed boundaries
✓ Monitor land use patterns  
✓ Track water quality metrics
✓ Identify priority areas
```

### 🔬 Environmental Research
```
✓ Analyze nutrient loads
✓ Study sediment transport
✓ Correlate land use with water quality
✓ Generate publication-ready visualizations
```

### 📊 Planning & Policy
```
✓ Create stakeholder presentations
✓ Support decision-making
✓ Evaluate scenarios
✓ Public engagement
```

### 🎓 Education & Training
```
✓ Teach GIS concepts
✓ Demonstrate spatial analysis
✓ Student projects
✓ Interactive learning
```

## 🎨 Example Workflows

### Explore Your Data
```bash
# 1. Generate sample data (or use your own)
python create_sample_data.py

# 2. Run dashboard
streamlit run watershed_dashboard.py

# 3. Load sample_data/watersheds.shp in browser
# 4. Explore through tabs
```

### Identify High-Risk Areas
```bash
# 1. Load your shapefile
# 2. Filter by high nitrogen loads
# 3. Color by forest percentage
# 4. Export filtered results to CSV
```

### Prepare Data for Analysis
```bash
# Validate your shapefile
python shapefile_utils.py validate watershed.shp

# Clean any issues
python shapefile_utils.py clean watershed.shp

# Simplify for performance
python shapefile_utils.py simplify watershed.shp 0.001

# Load in dashboard
```

## 🐳 Docker Deployment

### Single Command Start
```bash
docker-compose up watershed-dashboard
```

### Access Dashboard
```
http://localhost:8501
```

### Stop
```bash
docker-compose down
```

## 🔧 Customization

Edit `config.py` to customize:
- Dashboard title and icon
- Default map settings
- Color schemes
- Performance options
- Custom metrics

Example:
```python
DASHBOARD_TITLE = "My Watershed Project"
DEFAULT_BASE_MAP = 'Satellite'
COLOR_SCHEMES = ['Viridis', 'Blues', 'Greens']
```

## 📦 Installation Options

### Option 1: Python (Recommended)
```bash
pip install -r requirements.txt
streamlit run watershed_dashboard.py
```

### Option 2: Docker
```bash
docker-compose up watershed-dashboard
```

### Option 3: Cloud Deploy
Deploy to Streamlit Cloud (free):
1. Push to GitHub
2. Go to streamlit.io/cloud
3. Connect repository
4. Share link!

## 🧰 Utility Commands

```bash
# Get shapefile information
python shapefile_utils.py info watershed.shp

# Validate data quality
python shapefile_utils.py validate watershed.shp

# Clean and fix issues
python shapefile_utils.py clean watershed.shp

# Simplify geometries
python shapefile_utils.py simplify watershed.shp 0.001

# Convert to GeoJSON
python shapefile_utils.py geojson watershed.shp

# Reproject to WGS84
python shapefile_utils.py reproject watershed.shp EPSG:4326
```

## 📊 Sample Data

Generate realistic watershed data for testing:

```bash
python create_sample_data.py
```

Creates two shapefiles:
- **`sample_data/watersheds.shp`** - 15 basic watersheds
- **`sample_data/detailed_watersheds.shp`** - 20 sub-basins

Each includes 20+ attributes:
- Physical: Area, perimeter, elevation, slope
- Hydrologic: Stream length, discharge
- Land use: Forest, agriculture, urban percentages
- Water quality: Nitrogen, phosphorus, sediment loads
- Demographic: Population, density

## 🎓 Learning Resources

### Tutorials
1. **QUICKSTART.md** - Run your first dashboard
2. **VISUAL_GUIDE.md** - Learn the interface
3. **watershed_tutorial.ipynb** - Spatial analysis walkthrough

### Reference
- **WATERSHED_README.md** - Complete feature guide
- **PROJECT_SUMMARY.md** - Technical details
- Inline code comments

### External
- [GeoPandas Documentation](https://geopandas.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [USGS SPARROW](https://www.usgs.gov/mission-areas/water-resources/science/sparrow-mappers)

## 🤝 Comparison to USGS SPARROW

### Similar to SPARROW
✅ Interactive watershed visualization  
✅ Attribute-based mapping  
✅ Statistical summaries  
✅ Data filtering and export  
✅ Multiple base map layers  

### Additional Features
✅ General-purpose (any watershed shapefile)  
✅ Two framework options (Streamlit + Dash)  
✅ Data preprocessing utilities  
✅ Docker deployment  
✅ Sample data generator  
✅ Comprehensive documentation  

### Key Difference
SPARROW focuses on nutrient modeling with R.  
This dashboard is Python-based and works with any watershed shapefile.

## 📋 Requirements

- Python 3.8 or higher
- 2GB RAM (4GB recommended)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- ArcGIS shapefile (.shp, .shx, .dbf, .prj)

## 🐛 Troubleshooting

### Shapefile Won't Load
```bash
# Check if all required files are present
ls -l watershed.*

# Validate the shapefile
python shapefile_utils.py validate watershed.shp

# Clean if issues found
python shapefile_utils.py clean watershed.shp
```

### Map Not Displaying
```bash
# Check coordinate system
python shapefile_utils.py info watershed.shp

# Reproject to WGS84 if needed
python shapefile_utils.py reproject watershed.shp EPSG:4326
```

### Performance Issues
```bash
# Simplify large shapefiles
python shapefile_utils.py simplify watershed.shp 0.001
```

See [QUICKSTART.md](QUICKSTART.md) for more solutions.

## 🌟 Contributing

Contributions welcome! The code is:
- ✅ Well-documented with inline comments
- ✅ Modular and extensible
- ✅ Configuration-driven
- ✅ Following Python best practices

## 📄 License

Open source for educational and research purposes.

## 🙏 Acknowledgments

- Inspired by [USGS SPARROW mappers](https://www.usgs.gov/mission-areas/water-resources/science/sparrow-mappers)
- Built with [GeoPandas](https://geopandas.org/), [Streamlit](https://streamlit.io/), [Folium](https://python-visualization.github.io/folium/)
- Thanks to the open-source geospatial community

## 📞 Support

- **Documentation**: Start with [QUICKSTART.md](QUICKSTART.md)
- **Issues**: Check troubleshooting section
- **Questions**: See documentation files

## 🚀 Get Started Now!

```bash
# Clone or download this repository
# Install dependencies
pip install -r requirements.txt

# Generate sample data
python create_sample_data.py

# Run dashboard
streamlit run watershed_dashboard.py

# Open browser to http://localhost:8501
# Load sample_data/watersheds.shp
# Explore! 🎉
```

---

**Ready to visualize your watershed data?**  
Start with [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup guide!

---

Made with 💙 for the watershed community | [View Documentation](WATERSHED_README.md) | [Report Issues](https://github.com/gudaleon/2017-dlsl-msc-team1/issues)
