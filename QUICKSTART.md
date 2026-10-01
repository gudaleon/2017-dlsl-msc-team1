# Quick Start Guide - Watershed Dashboard

Get your watershed visualization dashboard running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Your watershed shapefile from ArcGIS

## Installation Steps

### Step 1: Install Dependencies

Choose either the Streamlit version (recommended for beginners) or Dash version:

**For Streamlit Dashboard:**
```bash
pip install -r requirements.txt
```

**For Dash Dashboard:**
```bash
pip install -r requirements_dash.txt
```

### Step 2: Verify Installation

Check that all packages are installed:
```bash
python -c "import geopandas, streamlit, folium; print('✅ All packages installed successfully!')"
```

## Running the Dashboard

### Option A: With Your Own Data

**Streamlit:**
```bash
streamlit run watershed_dashboard.py
```

Then:
1. Open browser to http://localhost:8501
2. Use the file uploader in the sidebar
3. Select all your shapefile components (.shp, .shx, .dbf, .prj)

**Dash:**
```bash
python watershed_dashboard_dash.py
```

Then:
1. Open browser to http://localhost:8050
2. Enter the path to your .shp file
3. Click "Load Data"

### Option B: With Sample Data

Create sample data first:
```bash
python create_sample_data.py
```

This creates two sample shapefiles:
- `sample_data/watersheds.shp` - Basic watersheds
- `sample_data/detailed_watersheds.shp` - Sub-basins

Then run the dashboard and load the sample file.

## Your First Dashboard

Once loaded, explore the tabs:

### 🗺️ Map Tab
- Pan and zoom the map
- Hover over watersheds to see attributes
- Toggle between base map layers
- Use the fullscreen button for better view

### 📊 Statistics Tab
- View summary statistics
- Explore distribution histograms
- Identify data patterns

### 📋 Data Table Tab
- Browse all attribute data
- Use search to find specific values
- Sort by any column
- Download filtered data as CSV

### ℹ️ Metadata Tab
- Check coordinate system
- View spatial extent
- Review attribute schema

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'geopandas'"

**Solution:** Install all requirements
```bash
pip install -r requirements.txt
```

### Issue: Shapefile won't load

**Solution:** Make sure you have all required files:
- watersheds.shp (main file)
- watersheds.shx (index file)
- watersheds.dbf (attributes)
- watersheds.prj (projection - recommended)

### Issue: "No CRS defined" warning

**Solution:** Your shapefile is missing projection information. The dashboard will assume WGS84 (EPSG:4326). To fix:
```bash
python shapefile_utils.py reproject your_file.shp EPSG:4326
```

### Issue: Map not displaying correctly

**Solution:** Try cleaning your shapefile:
```bash
python shapefile_utils.py clean your_file.shp
```

### Issue: Dashboard is slow with large shapefiles

**Solution:** Simplify the geometries:
```bash
python shapefile_utils.py simplify your_file.shp 0.001
```

## Shapefile Utilities

The `shapefile_utils.py` script provides helpful tools:

### Get Information
```bash
python shapefile_utils.py info your_file.shp
```

### Validate Shapefile
```bash
python shapefile_utils.py validate your_file.shp
```

### Clean Shapefile
```bash
python shapefile_utils.py clean your_file.shp
```

### Convert to GeoJSON
```bash
python shapefile_utils.py geojson your_file.shp
```

### Simplify Geometries
```bash
python shapefile_utils.py simplify your_file.shp 0.001
```

### Reproject to WGS84
```bash
python shapefile_utils.py reproject your_file.shp EPSG:4326
```

## Customization Tips

### Change Color Schemes

In the sidebar, try different color schemes:
- `YlOrRd` - Yellow to Red (good for continuous data)
- `Viridis` - Multi-hue (colorblind friendly)
- `RdYlGn` - Red-Yellow-Green (good for quality metrics)
- `Blues` - Single hue (good for water-related data)

### Filter Your Data

1. Select an attribute in "Filter by attribute"
2. Adjust the slider to focus on specific ranges
3. The map and statistics update automatically

### Color by Attribute

1. Choose "Color by attribute" in the sidebar
2. Select a numeric field (e.g., Area, Population, Nitrogen Load)
3. The map will show a choropleth visualization

### Export Your Data

1. Go to the Data Table tab
2. Use search to filter if needed
3. Click "Download as CSV"
4. Open in Excel or other tools

## Next Steps

### Add Your Own Analysis

Edit `watershed_dashboard.py` to add custom calculations:

```python
# Add after loading gdf
gdf['nitrogen_per_area'] = gdf['NITROGEN_KG'] / gdf['AREA_SQKM']
gdf['pop_density'] = gdf['POPULATION'] / gdf['AREA_SQKM']
```

### Integrate External Data

Load additional datasets and join with watersheds:

```python
# In watershed_dashboard.py
external_data = pd.read_csv('monitoring_data.csv')
gdf = gdf.merge(external_data, left_on='WATERSHED_ID', right_on='ID')
```

### Deploy Online

To share your dashboard:

**Streamlit Cloud (Free):**
1. Push code to GitHub
2. Go to streamlit.io/cloud
3. Connect your repo
4. Deploy!

**Heroku or AWS:**
See WATERSHED_README.md for deployment guides

## Learning Resources

- [GeoPandas Documentation](https://geopandas.org/) - Spatial data manipulation
- [Streamlit Gallery](https://streamlit.io/gallery) - Dashboard examples
- [Folium Documentation](https://python-visualization.github.io/folium/) - Interactive maps
- [USGS SPARROW](https://www.usgs.gov/mission-areas/water-resources/science/sparrow-mappers) - Reference implementation

## Getting Help

1. Check `WATERSHED_README.md` for detailed documentation
2. Use `shapefile_utils.py info` to diagnose data issues
3. Try the sample data to verify installation
4. Check the inline code comments for customization hints

## Example Workflow

Here's a complete workflow from raw data to dashboard:

```bash
# 1. Create sample data (or use your own)
python create_sample_data.py

# 2. Validate your shapefile
python shapefile_utils.py validate sample_data/watersheds.shp

# 3. Clean if needed
python shapefile_utils.py clean sample_data/watersheds.shp

# 4. Run dashboard
streamlit run watershed_dashboard.py

# 5. Load sample_data/watersheds.shp in the browser
# 6. Explore the data through different tabs
# 7. Customize colors and filters
# 8. Export results
```

## Success!

You should now have a working watershed dashboard! 

The dashboard provides:
- ✅ Interactive maps with multiple layers
- ✅ Statistical analysis
- ✅ Data filtering and search
- ✅ CSV export
- ✅ Multiple visualization options

Enjoy exploring your watershed data! 🌊
