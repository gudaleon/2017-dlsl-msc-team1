"""
Utility functions for working with ArcGIS shapefiles
Preprocessing, validation, and conversion tools
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path
import json
from shapely.validation import make_valid
from shapely.geometry import mapping

def validate_shapefile(shapefile_path):
    """
    Validate shapefile and report any issues
    
    Parameters:
    -----------
    shapefile_path : str
        Path to the shapefile
    
    Returns:
    --------
    dict : Validation report
    """
    
    report = {
        'valid': True,
        'warnings': [],
        'errors': [],
        'info': {}
    }
    
    try:
        gdf = gpd.read_file(shapefile_path)
        
        report['info']['feature_count'] = len(gdf)
        report['info']['column_count'] = len(gdf.columns)
        report['info']['crs'] = str(gdf.crs) if gdf.crs else 'Not defined'
        report['info']['geometry_types'] = gdf.geometry.geom_type.unique().tolist()
        
        if gdf.crs is None:
            report['warnings'].append("No coordinate reference system (CRS) defined")
        
        invalid_geoms = ~gdf.geometry.is_valid
        if invalid_geoms.any():
            count = invalid_geoms.sum()
            report['warnings'].append(f"{count} invalid geometries found")
            report['info']['invalid_geometry_indices'] = gdf[invalid_geoms].index.tolist()
        
        null_geoms = gdf.geometry.isna()
        if null_geoms.any():
            count = null_geoms.sum()
            report['errors'].append(f"{count} null geometries found")
            report['valid'] = False
        
        empty_geoms = gdf.geometry.is_empty
        if empty_geoms.any():
            count = empty_geoms.sum()
            report['warnings'].append(f"{count} empty geometries found")
        
        for col in gdf.columns:
            if col != 'geometry':
                null_count = gdf[col].isna().sum()
                if null_count > 0:
                    report['info'][f'null_values_{col}'] = null_count
        
        bounds = gdf.total_bounds
        report['info']['extent'] = {
            'minx': float(bounds[0]),
            'miny': float(bounds[1]),
            'maxx': float(bounds[2]),
            'maxy': float(bounds[3])
        }
        
    except Exception as e:
        report['valid'] = False
        report['errors'].append(f"Error reading shapefile: {str(e)}")
    
    return report

def clean_shapefile(input_path, output_path=None, fix_geometries=True, remove_nulls=True):
    """
    Clean and fix common shapefile issues
    
    Parameters:
    -----------
    input_path : str
        Path to input shapefile
    output_path : str, optional
        Path for cleaned shapefile (default: adds '_cleaned' to filename)
    fix_geometries : bool
        Whether to fix invalid geometries
    remove_nulls : bool
        Whether to remove features with null geometries
    
    Returns:
    --------
    GeoDataFrame : Cleaned data
    """
    
    print(f"Reading shapefile: {input_path}")
    gdf = gpd.read_file(input_path)
    
    original_count = len(gdf)
    print(f"Original feature count: {original_count}")
    
    if remove_nulls:
        null_mask = gdf.geometry.isna()
        if null_mask.any():
            null_count = null_mask.sum()
            gdf = gdf[~null_mask]
            print(f"Removed {null_count} features with null geometries")
    
    empty_mask = gdf.geometry.is_empty
    if empty_mask.any():
        empty_count = empty_mask.sum()
        gdf = gdf[~empty_mask]
        print(f"Removed {empty_count} features with empty geometries")
    
    if fix_geometries:
        invalid_mask = ~gdf.geometry.is_valid
        if invalid_mask.any():
            invalid_count = invalid_mask.sum()
            print(f"Fixing {invalid_count} invalid geometries")
            gdf.geometry = gdf.geometry.apply(lambda geom: make_valid(geom) if not geom.is_valid else geom)
    
    if gdf.crs is None:
        print("Warning: No CRS defined. Setting to WGS84 (EPSG:4326)")
        gdf = gdf.set_crs("EPSG:4326")
    
    final_count = len(gdf)
    print(f"Final feature count: {final_count}")
    
    if output_path is None:
        input_path_obj = Path(input_path)
        output_path = input_path_obj.parent / f"{input_path_obj.stem}_cleaned.shp"
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    gdf.to_file(output_path)
    print(f"Cleaned shapefile saved to: {output_path}")
    
    return gdf

def convert_to_geojson(shapefile_path, output_path=None):
    """
    Convert shapefile to GeoJSON format
    
    Parameters:
    -----------
    shapefile_path : str
        Path to input shapefile
    output_path : str, optional
        Path for GeoJSON output
    """
    
    gdf = gpd.read_file(shapefile_path)
    
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    else:
        gdf = gdf.to_crs("EPSG:4326")
    
    if output_path is None:
        output_path = Path(shapefile_path).with_suffix('.geojson')
    
    gdf.to_file(output_path, driver='GeoJSON')
    print(f"GeoJSON saved to: {output_path}")
    
    return output_path

def simplify_geometries(shapefile_path, output_path=None, tolerance=0.001):
    """
    Simplify geometries to reduce file size and improve performance
    
    Parameters:
    -----------
    shapefile_path : str
        Path to input shapefile
    output_path : str, optional
        Path for simplified output
    tolerance : float
        Simplification tolerance (smaller = more detail)
    """
    
    print(f"Reading shapefile: {shapefile_path}")
    gdf = gpd.read_file(shapefile_path)
    
    original_coords = sum(len(list(geom.exterior.coords)) for geom in gdf.geometry if hasattr(geom, 'exterior'))
    
    print(f"Simplifying geometries with tolerance={tolerance}")
    gdf.geometry = gdf.geometry.simplify(tolerance, preserve_topology=True)
    
    simplified_coords = sum(len(list(geom.exterior.coords)) for geom in gdf.geometry if hasattr(geom, 'exterior'))
    
    if original_coords > 0:
        reduction = (1 - simplified_coords / original_coords) * 100
        print(f"Coordinate reduction: {reduction:.1f}%")
    
    if output_path is None:
        input_path_obj = Path(shapefile_path)
        output_path = input_path_obj.parent / f"{input_path_obj.stem}_simplified.shp"
    
    gdf.to_file(output_path)
    print(f"Simplified shapefile saved to: {output_path}")
    
    return gdf

def reproject_shapefile(shapefile_path, target_crs='EPSG:4326', output_path=None):
    """
    Reproject shapefile to a different coordinate reference system
    
    Parameters:
    -----------
    shapefile_path : str
        Path to input shapefile
    target_crs : str
        Target CRS (default: WGS84)
    output_path : str, optional
        Path for reprojected output
    """
    
    gdf = gpd.read_file(shapefile_path)
    
    if gdf.crs is None:
        print("Warning: Input shapefile has no CRS. Assuming WGS84.")
        gdf = gdf.set_crs("EPSG:4326")
    
    print(f"Reprojecting from {gdf.crs} to {target_crs}")
    gdf = gdf.to_crs(target_crs)
    
    if output_path is None:
        input_path_obj = Path(shapefile_path)
        crs_suffix = target_crs.replace(':', '_').replace('+', '').replace(' ', '_')
        output_path = input_path_obj.parent / f"{input_path_obj.stem}_{crs_suffix}.shp"
    
    gdf.to_file(output_path)
    print(f"Reprojected shapefile saved to: {output_path}")
    
    return gdf

def get_shapefile_info(shapefile_path, detailed=False):
    """
    Get detailed information about a shapefile
    
    Parameters:
    -----------
    shapefile_path : str
        Path to shapefile
    detailed : bool
        Include detailed attribute statistics
    """
    
    gdf = gpd.read_file(shapefile_path)
    
    info = {
        'path': str(shapefile_path),
        'feature_count': len(gdf),
        'columns': len(gdf.columns) - 1,
        'crs': str(gdf.crs) if gdf.crs else 'Not defined',
        'geometry_types': gdf.geometry.geom_type.unique().tolist(),
        'bounds': {
            'minx': float(gdf.total_bounds[0]),
            'miny': float(gdf.total_bounds[1]),
            'maxx': float(gdf.total_bounds[2]),
            'maxy': float(gdf.total_bounds[3])
        }
    }
    
    info['column_info'] = {}
    for col in gdf.columns:
        if col != 'geometry':
            col_info = {
                'dtype': str(gdf[col].dtype),
                'null_count': int(gdf[col].isna().sum()),
                'unique_values': int(gdf[col].nunique())
            }
            
            if detailed and pd.api.types.is_numeric_dtype(gdf[col]):
                col_info.update({
                    'min': float(gdf[col].min()) if not gdf[col].isna().all() else None,
                    'max': float(gdf[col].max()) if not gdf[col].isna().all() else None,
                    'mean': float(gdf[col].mean()) if not gdf[col].isna().all() else None,
                    'median': float(gdf[col].median()) if not gdf[col].isna().all() else None
                })
            
            info['column_info'][col] = col_info
    
    return info

def print_shapefile_info(shapefile_path):
    """Print formatted shapefile information"""
    
    info = get_shapefile_info(shapefile_path, detailed=True)
    
    print("=" * 60)
    print(f"SHAPEFILE INFORMATION")
    print("=" * 60)
    print(f"Path: {info['path']}")
    print(f"Features: {info['feature_count']}")
    print(f"Attributes: {info['columns']}")
    print(f"CRS: {info['crs']}")
    print(f"Geometry Types: {', '.join(info['geometry_types'])}")
    print(f"\nSpatial Extent:")
    print(f"  Min X: {info['bounds']['minx']:.6f}")
    print(f"  Min Y: {info['bounds']['miny']:.6f}")
    print(f"  Max X: {info['bounds']['maxx']:.6f}")
    print(f"  Max Y: {info['bounds']['maxy']:.6f}")
    print(f"\nAttribute Information:")
    print("-" * 60)
    
    for col, col_info in info['column_info'].items():
        print(f"\n{col}:")
        print(f"  Type: {col_info['dtype']}")
        print(f"  Unique: {col_info['unique_values']}")
        print(f"  Nulls: {col_info['null_count']}")
        
        if 'mean' in col_info:
            print(f"  Range: {col_info['min']:.2f} - {col_info['max']:.2f}")
            print(f"  Mean: {col_info['mean']:.2f}")
            print(f"  Median: {col_info['median']:.2f}")
    
    print("=" * 60)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python shapefile_utils.py <command> <shapefile_path> [options]")
        print("\nCommands:")
        print("  info <path>              - Display shapefile information")
        print("  validate <path>          - Validate shapefile and report issues")
        print("  clean <path>             - Clean and fix shapefile issues")
        print("  simplify <path> [tol]    - Simplify geometries (default tolerance: 0.001)")
        print("  reproject <path> [crs]   - Reproject to CRS (default: EPSG:4326)")
        print("  geojson <path>           - Convert to GeoJSON")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if len(sys.argv) < 3:
        print("Error: Shapefile path required")
        sys.exit(1)
    
    shapefile_path = sys.argv[2]
    
    if not Path(shapefile_path).exists():
        print(f"Error: File not found: {shapefile_path}")
        sys.exit(1)
    
    if command == 'info':
        print_shapefile_info(shapefile_path)
    
    elif command == 'validate':
        report = validate_shapefile(shapefile_path)
        print(json.dumps(report, indent=2))
    
    elif command == 'clean':
        clean_shapefile(shapefile_path)
    
    elif command == 'simplify':
        tolerance = float(sys.argv[3]) if len(sys.argv) > 3 else 0.001
        simplify_geometries(shapefile_path, tolerance=tolerance)
    
    elif command == 'reproject':
        target_crs = sys.argv[3] if len(sys.argv) > 3 else 'EPSG:4326'
        reproject_shapefile(shapefile_path, target_crs=target_crs)
    
    elif command == 'geojson':
        convert_to_geojson(shapefile_path)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
