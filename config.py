"""
Configuration file for Watershed Dashboard
Customize these settings for your specific needs
"""

# Dashboard Configuration
DASHBOARD_TITLE = "Watershed Analysis Dashboard"
DASHBOARD_ICON = "🌊"
PAGE_LAYOUT = "wide"

# Map Configuration
DEFAULT_MAP_CENTER = [40.0, -95.0]
DEFAULT_ZOOM = 8
DEFAULT_BASE_MAP = 'OpenStreetMap'

# Available base map tiles
BASE_MAPS = {
    'OpenStreetMap': 'OpenStreetMap',
    'Terrain': 'Stamen Terrain',
    'Light': 'CartoDB positron',
    'Dark': 'CartoDB dark_matter',
    'Satellite': 'Esri WorldImagery'
}

# Color Schemes for Choropleth Maps
COLOR_SCHEMES = [
    'YlOrRd',
    'YlGnBu', 
    'RdYlGn',
    'Viridis',
    'Plasma',
    'Blues',
    'Reds',
    'Greens',
    'Purples',
    'Oranges'
]

# Data Configuration
DEFAULT_CRS = 'EPSG:4326'
MAX_UPLOAD_SIZE_MB = 200
TEMP_UPLOAD_DIR = '/tmp/shapefile_upload'

# Display Configuration
MAX_TABLE_ROWS = 1000
MAX_CHART_COLUMNS = 8
HISTOGRAM_BINS = 30

# Attribute Display Names (customize for your data)
ATTRIBUTE_LABELS = {
    'AREA_SQKM': 'Area (km²)',
    'PERIMETER_KM': 'Perimeter (km)',
    'AVG_ELEVATION': 'Average Elevation (m)',
    'AVG_SLOPE': 'Average Slope (%)',
    'STREAM_LENGTH': 'Stream Length (km)',
    'STREAM_DENSITY': 'Stream Density (km/km²)',
    'ANNUAL_PRECIP': 'Annual Precipitation (mm)',
    'MEAN_TEMP': 'Mean Temperature (°C)',
    'FOREST_PCT': 'Forest Cover (%)',
    'AGRICULTURE_PCT': 'Agriculture (%)',
    'URBAN_PCT': 'Urban (%)',
    'WETLAND_PCT': 'Wetland (%)',
    'POPULATION': 'Population',
    'POP_DENSITY': 'Population Density (per km²)',
    'NITROGEN_KG': 'Nitrogen Load (kg/yr)',
    'PHOSPHORUS_KG': 'Phosphorus Load (kg/yr)',
    'SEDIMENT_TONS': 'Sediment Load (tons/yr)',
    'DISCHARGE_CMS': 'Stream Discharge (m³/s)',
    'WATER_QUALITY': 'Water Quality Index'
}

# Attribute Units
ATTRIBUTE_UNITS = {
    'AREA_SQKM': 'km²',
    'PERIMETER_KM': 'km',
    'AVG_ELEVATION': 'm',
    'AVG_SLOPE': '%',
    'STREAM_LENGTH': 'km',
    'STREAM_DENSITY': 'km/km²',
    'ANNUAL_PRECIP': 'mm',
    'MEAN_TEMP': '°C',
    'NITROGEN_KG': 'kg/yr',
    'PHOSPHORUS_KG': 'kg/yr',
    'SEDIMENT_TONS': 'tons/yr',
    'DISCHARGE_CMS': 'm³/s'
}

# Tooltip Configuration
MAX_TOOLTIP_FIELDS = 5
TOOLTIP_PRIORITY_FIELDS = [
    'WATERSHED_ID',
    'NAME',
    'AREA_SQKM',
    'WATER_QUALITY',
    'POPULATION'
]

# Statistics Configuration
STATISTICS_TO_CALCULATE = [
    'mean',
    'median',
    'std',
    'min',
    'max',
    'count'
]

# Export Configuration
EXPORT_FORMATS = ['CSV', 'GeoJSON', 'Shapefile']
DEFAULT_EXPORT_FORMAT = 'CSV'

# Advanced Features
ENABLE_FILTERING = True
ENABLE_SEARCH = True
ENABLE_EXPORT = True
ENABLE_STATISTICS = True
ENABLE_CHOROPLETH = True

# Performance Settings
SIMPLIFY_TOLERANCE = 0.001
MAX_FEATURES_FOR_FULL_RENDER = 1000

# Custom Metrics (add your own calculations)
CUSTOM_METRICS = {
    'nutrient_ratio': {
        'formula': lambda gdf: gdf['NITROGEN_KG'] / gdf['PHOSPHORUS_KG'] if 'NITROGEN_KG' in gdf.columns and 'PHOSPHORUS_KG' in gdf.columns else None,
        'label': 'N:P Ratio',
        'unit': ''
    },
    'yield_per_area': {
        'formula': lambda gdf: gdf['NITROGEN_KG'] / gdf['AREA_SQKM'] if 'NITROGEN_KG' in gdf.columns and 'AREA_SQKM' in gdf.columns else None,
        'label': 'Nitrogen Yield',
        'unit': 'kg/km²/yr'
    }
}

# Validation Rules
VALIDATION_RULES = {
    'min_area': 0.1,
    'max_area': 100000,
    'min_slope': 0,
    'max_slope': 90
}

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# API Configuration (for future features)
ENABLE_API = False
API_PORT = 8000

# Database Configuration (for future features)
ENABLE_DATABASE = False
DATABASE_URL = None

# Help Text
HELP_TEXT = {
    'map': "Interactive map showing watershed boundaries. Hover over features for details.",
    'statistics': "Summary statistics and distribution charts for numeric attributes.",
    'data_table': "Browse, search, and export attribute data.",
    'metadata': "Technical information about the dataset including CRS and schema.",
    'color_by': "Select a numeric attribute to create a choropleth map.",
    'filter': "Filter features by attribute value ranges.",
    'upload': "Upload all shapefile components (.shp, .shx, .dbf, .prj)."
}
