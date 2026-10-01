# 🌊 Watershed Analysis Dashboard

Interactive visualization dashboard for ArcGIS shapefile data with watershed boundaries and attributes, inspired by USGS SPARROW mappers.

## Overview

This project provides two interactive dashboard implementations for visualizing and analyzing watershed data from ArcGIS shapefiles:

1. **Streamlit Dashboard** (`watershed_dashboard.py`) - User-friendly, quick to deploy
2. **Plotly Dash Dashboard** (`watershed_dashboard_dash.py`) - More customizable, production-ready

Both dashboards offer:
- 🗺️ Interactive maps with watershed boundaries
- 📊 Statistical analysis and visualizations
- 📋 Searchable data tables
- 🎨 Choropleth mapping for numeric attributes
- 📥 Data export capabilities
- ℹ️ Dataset metadata and schema information

## Features

### Map Visualization
- Multiple base map layers (Street, Terrain, Light)
- Interactive tooltips showing attribute data
- Zoom, pan, and measure tools
- Choropleth coloring by numeric attributes
- Fullscreen mode

### Statistical Analysis
- Summary statistics (mean, median, std dev, min, max)
- Distribution histograms for numeric attributes
- Customizable visualizations

### Data Management
- Upload shapefiles or load from file path
- Filter data by attribute ranges
- Search across all attributes
- Export filtered data to CSV

### Metadata
- Coordinate system information
- Spatial extent (bounding box)
- Attribute schema with data types
- Feature counts and statistics

## Installation

### Option 1: Streamlit Dashboard

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run watershed_dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Option 2: Dash Dashboard

```bash
# Install dependencies
pip install -r requirements_dash.txt

# Run the dashboard
python watershed_dashboard_dash.py
```

The dashboard will be available at `http://localhost:8050`

## Usage

### Uploading Data

#### Using File Upload (Streamlit only)
1. Click "Browse files" in the sidebar
2. Select all shapefile components (.shp, .shx, .dbf, .prj)
3. The data will load automatically

#### Using File Path (Both versions)
1. Enter the full path to your `.shp` file
2. Click "Load Data" (Dash) or press Enter (Streamlit)
3. Example: `/path/to/watersheds.shp`

### Exploring the Dashboard

#### Map Tab
- View watershed boundaries on an interactive map
- Toggle between different base layers
- Use measurement tools to calculate distances
- Hover over watersheds to see attribute data

#### Statistics Tab
- View summary statistics for all numeric attributes
- Explore distribution histograms
- Identify patterns and outliers

#### Data Table Tab
- Browse all attribute data in tabular format
- Search for specific values
- Sort by any column
- Export filtered data to CSV

#### Metadata Tab
- View coordinate system information
- Check spatial extent
- Review attribute schema and data types

### Customization Options

#### Color Mapping
In the sidebar, select:
- **Color by attribute**: Choose a numeric field for choropleth mapping
- **Color scheme**: Pick from various color palettes (YlOrRd, Viridis, Blues, etc.)

#### Filtering
- **Filter by attribute**: Select a numeric field to filter
- **Range slider**: Adjust the range to show only relevant features

## Shapefile Requirements

Your shapefile should include:
- `.shp` - Main geometry file (required)
- `.shx` - Shape index file (required)
- `.dbf` - Attribute database (required)
- `.prj` - Projection information (recommended)

The dashboard supports:
- Polygon and MultiPolygon geometries
- Any coordinate reference system (auto-converted to WGS84 for display)
- Multiple numeric and categorical attributes

## Example Data Structure

```
watersheds/
├── watersheds.shp
├── watersheds.shx
├── watersheds.dbf
└── watersheds.prj
```

Typical attributes might include:
- Watershed ID or name
- Area (sq km)
- Stream length
- Average slope
- Land use percentages
- Water quality metrics
- Population

## Comparison to USGS SPARROW

This dashboard is inspired by the USGS SPARROW (SPAtially Referenced Regressions On Watershed attributes) mappers, which provide:
- Interactive watershed mapping
- Nutrient and sediment load visualization
- Source contribution analysis
- Scenario evaluation tools

Our implementation provides similar visualization capabilities for your custom watershed data, with:
- Flexible attribute mapping
- Multiple visualization options
- Easy data filtering and export
- Customizable appearance

## Technology Stack

- **GeoPandas**: Spatial data manipulation
- **Folium**: Interactive mapping (Streamlit version)
- **Plotly**: Charts and maps (Dash version)
- **Streamlit**: Web application framework (Option 1)
- **Dash**: Web application framework (Option 2)
- **Pandas**: Data analysis

## Troubleshooting

### Issue: Shapefile won't load
- Ensure all required files (.shp, .shx, .dbf) are present
- Check that the file path is correct
- Verify the shapefile is not corrupted

### Issue: Map not displaying correctly
- Check that your shapefile has valid geometries
- Ensure coordinate system is defined in .prj file
- Try reloading the data

### Issue: No numeric columns for analysis
- Verify your .dbf file contains numeric fields
- Check that data types are correctly set in ArcGIS

### Issue: Performance with large datasets
- Consider simplifying geometries before loading
- Filter data to focus on specific regions
- Use the Dash version for better performance with large datasets

## Advanced Usage

### Programmatic Access

You can also use the dashboard functions programmatically:

```python
import geopandas as gpd
from watershed_dashboard import load_shapefile, create_map, create_summary_statistics

# Load your data
gdf = load_shapefile('/path/to/watersheds.shp')

# Create visualizations
map_obj = create_map(gdf, selected_column='area', color_scheme='YlOrRd')

# Generate statistics
stats = create_summary_statistics(gdf, gdf.select_dtypes(include=['number']).columns)
```

### Customizing the Dashboard

Both dashboard files are well-documented and can be customized:
- Add new visualization types
- Integrate with external APIs
- Add custom analysis functions
- Modify color schemes and styles

## References

- [USGS RSPARROW](https://github.com/USGS-R/RSPARROW) - Official SPARROW R package
- [SPARROW Mappers](https://www.usgs.gov/mission-areas/water-resources/science/sparrow-mappers) - USGS interactive mappers
- [GeoPandas Documentation](https://geopandas.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Dash Documentation](https://dash.plotly.com/)

## Contributing

To add features or report issues:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available for educational and research purposes.

## Support

For questions or issues:
- Check the Troubleshooting section above
- Review the inline code documentation
- Consult the referenced documentation links

---

Created with inspiration from USGS SPARROW watershed analysis tools.
