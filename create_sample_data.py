"""
Create sample watershed shapefile for testing the dashboard
This generates synthetic watershed data with realistic attributes
"""

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
import numpy as np
from pathlib import Path

def create_sample_watersheds(output_path='sample_data/watersheds.shp', num_watersheds=15):
    """
    Create a sample watershed shapefile with realistic attributes
    
    Parameters:
    -----------
    output_path : str
        Path where the shapefile will be saved
    num_watersheds : int
        Number of watershed polygons to generate
    """
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    np.random.seed(42)
    
    watersheds = []
    attributes = []
    
    base_lat = 40.0
    base_lon = -95.0
    grid_size = 0.5
    
    for i in range(num_watersheds):
        row = i // 4
        col = i % 4
        
        offset_x = np.random.uniform(-0.05, 0.05)
        offset_y = np.random.uniform(-0.05, 0.05)
        
        x = base_lon + col * grid_size + offset_x
        y = base_lat + row * grid_size + offset_y
        
        width = np.random.uniform(0.3, 0.6)
        height = np.random.uniform(0.3, 0.6)
        
        coords = [
            (x, y),
            (x + width, y),
            (x + width * 1.1, y + height * 0.5),
            (x + width, y + height),
            (x, y + height * 0.9),
            (x - width * 0.1, y + height * 0.5),
            (x, y)
        ]
        
        polygon = Polygon(coords)
        watersheds.append(polygon)
        
        area_sqkm = np.random.uniform(50, 500)
        
        attrs = {
            'WATERSHED_ID': f'WS_{i+1:03d}',
            'NAME': f'Watershed {chr(65 + i % 26)}{i // 26 + 1}',
            'AREA_SQKM': round(area_sqkm, 2),
            'PERIMETER_KM': round(np.random.uniform(30, 100), 2),
            'AVG_ELEVATION': round(np.random.uniform(200, 1500), 1),
            'AVG_SLOPE': round(np.random.uniform(2, 25), 2),
            'STREAM_LENGTH': round(np.random.uniform(10, 80), 2),
            'STREAM_DENSITY': round(np.random.uniform(0.5, 2.5), 3),
            'ANNUAL_PRECIP': round(np.random.uniform(400, 1200), 1),
            'MEAN_TEMP': round(np.random.uniform(8, 18), 1),
            'FOREST_PCT': round(np.random.uniform(10, 80), 1),
            'AGRICULTURE_PCT': round(np.random.uniform(5, 60), 1),
            'URBAN_PCT': round(np.random.uniform(1, 30), 1),
            'WETLAND_PCT': round(np.random.uniform(0, 15), 1),
            'POPULATION': int(np.random.uniform(1000, 50000)),
            'POP_DENSITY': round(np.random.uniform(10, 200), 1),
            'NITROGEN_KG': round(np.random.uniform(1000, 15000), 1),
            'PHOSPHORUS_KG': round(np.random.uniform(100, 2000), 1),
            'SEDIMENT_TONS': round(np.random.uniform(500, 8000), 1),
            'DISCHARGE_CMS': round(np.random.uniform(0.5, 15), 2),
            'WATER_QUALITY': np.random.choice(['Excellent', 'Good', 'Fair', 'Poor'], 
                                            p=[0.2, 0.4, 0.3, 0.1]),
            'MONITORING_SITES': int(np.random.uniform(1, 8)),
            'LAST_SURVEY': np.random.choice(['2023', '2022', '2021', '2020']),
        }
        
        attributes.append(attrs)
    
    gdf = gpd.GeoDataFrame(attributes, geometry=watersheds, crs='EPSG:4326')
    
    gdf.to_file(output_path)
    
    print(f"✅ Sample watershed data created successfully!")
    print(f"📁 Location: {output_path.absolute()}")
    print(f"📊 Features: {len(gdf)}")
    print(f"📋 Attributes: {len(gdf.columns) - 1}")
    print(f"\nAttribute Summary:")
    print("-" * 50)
    
    numeric_cols = gdf.select_dtypes(include=['number']).columns
    for col in numeric_cols[:5]:
        print(f"{col:20s}: {gdf[col].min():.2f} - {gdf[col].max():.2f}")
    
    print("\nYou can now use this file with the watershed dashboard:")
    print(f"  streamlit run watershed_dashboard.py")
    print(f"\nOr load it directly by entering this path in the dashboard:")
    print(f"  {output_path.absolute()}")
    
    return gdf

def create_sample_with_subbasins(output_path='sample_data/detailed_watersheds.shp'):
    """
    Create a more complex sample with nested sub-basins
    """
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    np.random.seed(123)
    
    main_basin = Polygon([
        (-96.0, 40.0),
        (-94.0, 40.0),
        (-94.0, 41.5),
        (-96.0, 41.5),
        (-96.0, 40.0)
    ])
    
    watersheds = []
    attributes = []
    
    subbasin_width = 0.4
    subbasin_height = 0.3
    
    basin_id = 1
    
    for i in range(5):
        for j in range(4):
            x = -96.0 + 0.1 + j * (subbasin_width + 0.1)
            y = 40.0 + 0.1 + i * (subbasin_height + 0.1)
            
            coords = [
                (x, y),
                (x + subbasin_width, y),
                (x + subbasin_width, y + subbasin_height),
                (x, y + subbasin_height),
                (x, y)
            ]
            
            polygon = Polygon(coords)
            
            if polygon.within(main_basin) or polygon.intersects(main_basin):
                watersheds.append(polygon)
                
                attrs = {
                    'BASIN_ID': f'B{basin_id:03d}',
                    'BASIN_NAME': f'Sub-basin {basin_id}',
                    'AREA_KM2': round(polygon.area * 111 * 111, 2),
                    'OUTLET_ELEV': round(300 + np.random.uniform(-50, 50), 1),
                    'MAX_ELEV': round(800 + np.random.uniform(-100, 200), 1),
                    'RELIEF': round(np.random.uniform(200, 600), 1),
                    'STREAM_ORDER': int(np.random.uniform(1, 5)),
                    'FLOW_CMS': round(np.random.uniform(0.1, 10), 2),
                    'TN_LOAD': round(np.random.uniform(500, 8000), 1),
                    'TP_LOAD': round(np.random.uniform(50, 800), 1),
                    'IMPERV_PCT': round(np.random.uniform(5, 45), 1),
                    'LANDUSE_DOM': np.random.choice(['Agriculture', 'Forest', 'Urban', 'Mixed']),
                }
                
                attributes.append(attrs)
                basin_id += 1
    
    gdf = gpd.GeoDataFrame(attributes, geometry=watersheds, crs='EPSG:4326')
    
    gdf.to_file(output_path)
    
    print(f"✅ Detailed watershed data created successfully!")
    print(f"📁 Location: {output_path.absolute()}")
    print(f"📊 Features: {len(gdf)}")
    
    return gdf

if __name__ == "__main__":
    print("Creating sample watershed data...\n")
    
    print("1. Creating basic watershed sample:")
    print("=" * 50)
    gdf1 = create_sample_watersheds()
    
    print("\n" + "=" * 50)
    print("2. Creating detailed sub-basin sample:")
    print("=" * 50)
    gdf2 = create_sample_with_subbasins()
    
    print("\n" + "=" * 50)
    print("✨ All sample data created successfully!")
    print("\nBoth shapefiles are ready to use with the dashboard.")
