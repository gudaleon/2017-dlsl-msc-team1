"""
Watershed Dashboard Application
Interactive visualization tool for watershed boundaries and attribute data from ArcGIS shapefiles.
Similar to USGS SPARROW mappers.
"""

import streamlit as st
import geopandas as gpd
import folium
from folium import plugins
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Watershed Analysis Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_shapefile(filepath):
    """Load shapefile and return GeoDataFrame"""
    try:
        gdf = gpd.read_file(filepath)
        return gdf
    except Exception as e:
        st.error(f"Error loading shapefile: {str(e)}")
        return None

def create_map(gdf, selected_column=None, color_scheme='YlOrRd'):
    """Create interactive folium map with watershed boundaries"""
    
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    else:
        gdf = gdf.to_crs("EPSG:4326")
    
    center_lat = gdf.geometry.centroid.y.mean()
    center_lon = gdf.geometry.centroid.x.mean()
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=8,
        tiles=None
    )
    
    folium.TileLayer('OpenStreetMap', name='Street Map').add_to(m)
    folium.TileLayer('Stamen Terrain', name='Terrain').add_to(m)
    folium.TileLayer('CartoDB positron', name='Light').add_to(m)
    
    if selected_column and selected_column in gdf.columns:
        if pd.api.types.is_numeric_dtype(gdf[selected_column]):
            folium.Choropleth(
                geo_data=gdf,
                data=gdf,
                columns=['geometry', selected_column],
                key_on='feature.id',
                fill_color=color_scheme,
                fill_opacity=0.7,
                line_opacity=0.3,
                legend_name=selected_column,
                name='Choropleth Layer'
            ).add_to(m)
    
    style_function = lambda x: {
        'fillColor': '#3388ff',
        'color': '#000000',
        'weight': 2,
        'fillOpacity': 0.5,
    }
    
    highlight_function = lambda x: {
        'fillColor': '#ffff00',
        'color': '#000000',
        'weight': 3,
        'fillOpacity': 0.7,
    }
    
    tooltip_fields = [col for col in gdf.columns if col != 'geometry'][:5]
    
    geojson = folium.GeoJson(
        gdf,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=tooltip_fields,
            aliases=[str(field) for field in tooltip_fields],
            localize=True
        ),
        name='Watersheds'
    )
    geojson.add_to(m)
    
    plugins.Fullscreen(
        position='topright',
        title='Expand map',
        title_cancel='Exit fullscreen',
        force_separate_button=True
    ).add_to(m)
    
    plugins.MeasureControl(position='topleft').add_to(m)
    
    folium.LayerControl().add_to(m)
    
    return m

def create_statistics_charts(gdf, numeric_columns):
    """Create statistical visualizations for numeric attributes"""
    charts = []
    
    for col in numeric_columns[:4]:
        fig = px.histogram(
            gdf, 
            x=col, 
            title=f'Distribution of {col}',
            nbins=30,
            color_discrete_sequence=['#1f77b4']
        )
        fig.update_layout(
            xaxis_title=col,
            yaxis_title='Count',
            height=300
        )
        charts.append((col, fig))
    
    return charts

def create_summary_statistics(gdf, numeric_columns):
    """Generate summary statistics table"""
    stats_data = []
    
    for col in numeric_columns:
        stats = {
            'Attribute': col,
            'Mean': f"{gdf[col].mean():.2f}",
            'Median': f"{gdf[col].median():.2f}",
            'Std Dev': f"{gdf[col].std():.2f}",
            'Min': f"{gdf[col].min():.2f}",
            'Max': f"{gdf[col].max():.2f}",
            'Count': len(gdf[col].dropna())
        }
        stats_data.append(stats)
    
    return pd.DataFrame(stats_data)

def main():
    st.title("🌊 Watershed Analysis Dashboard")
    st.markdown("""
    Interactive dashboard for visualizing watershed boundaries and analyzing spatial data.
    Upload your ArcGIS shapefile to explore watershed characteristics and patterns.
    """)
    
    with st.sidebar:
        st.header("📁 Data Input")
        
        uploaded_files = st.file_uploader(
            "Upload Shapefile Components",
            type=['shp', 'shx', 'dbf', 'prj', 'cpg'],
            accept_multiple_files=True,
            help="Upload all shapefile components (.shp, .shx, .dbf, .prj)"
        )
        
        gdf = None
        
        if uploaded_files:
            temp_dir = Path("/tmp/shapefile_upload")
            temp_dir.mkdir(exist_ok=True)
            
            for uploaded_file in uploaded_files:
                file_path = temp_dir / uploaded_file.name
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            
            shp_files = list(temp_dir.glob("*.shp"))
            if shp_files:
                gdf = load_shapefile(str(shp_files[0]))
                st.success(f"✅ Loaded: {shp_files[0].name}")
        
        shapefile_path = st.text_input(
            "Or enter shapefile path:",
            placeholder="/path/to/watersheds.shp",
            help="Enter the full path to your shapefile"
        )
        
        if shapefile_path and Path(shapefile_path).exists():
            gdf = load_shapefile(shapefile_path)
            if gdf is not None:
                st.success(f"✅ Loaded from path")
    
    if gdf is not None:
        with st.sidebar:
            st.header("🎨 Visualization Options")
            
            numeric_columns = gdf.select_dtypes(include=['number']).columns.tolist()
            
            if numeric_columns:
                color_column = st.selectbox(
                    "Color by attribute:",
                    options=['None'] + numeric_columns,
                    help="Select a numeric attribute for choropleth mapping"
                )
                
                if color_column != 'None':
                    color_scheme = st.selectbox(
                        "Color scheme:",
                        options=['YlOrRd', 'YlGnBu', 'RdYlGn', 'Viridis', 'Plasma', 'Blues', 'Reds', 'Greens']
                    )
                else:
                    color_column = None
                    color_scheme = 'YlOrRd'
            else:
                color_column = None
                color_scheme = 'YlOrRd'
            
            st.header("📊 Filter Options")
            
            if numeric_columns:
                filter_column = st.selectbox(
                    "Filter by attribute:",
                    options=['None'] + numeric_columns
                )
                
                if filter_column != 'None':
                    min_val = float(gdf[filter_column].min())
                    max_val = float(gdf[filter_column].max())
                    
                    filter_range = st.slider(
                        f"Select {filter_column} range:",
                        min_value=min_val,
                        max_value=max_val,
                        value=(min_val, max_val)
                    )
                    
                    gdf = gdf[
                        (gdf[filter_column] >= filter_range[0]) & 
                        (gdf[filter_column] <= filter_range[1])
                    ]
        
        tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Map", "📊 Statistics", "📋 Data Table", "ℹ️ Metadata"])
        
        with tab1:
            st.header("Watershed Map")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Watersheds", len(gdf))
            with col2:
                total_area = gdf.geometry.area.sum()
                st.metric("Total Area", f"{total_area:.2f} sq units")
            with col3:
                if numeric_columns:
                    avg_val = gdf[numeric_columns[0]].mean()
                    st.metric(f"Avg {numeric_columns[0]}", f"{avg_val:.2f}")
            
            map_obj = create_map(gdf, color_column, color_scheme)
            st_folium(map_obj, width=1200, height=600)
        
        with tab2:
            st.header("Statistical Analysis")
            
            if numeric_columns:
                st.subheader("Summary Statistics")
                summary_stats = create_summary_statistics(gdf, numeric_columns)
                st.dataframe(summary_stats, use_container_width=True)
                
                st.subheader("Distribution Charts")
                charts = create_statistics_charts(gdf, numeric_columns)
                
                cols = st.columns(2)
                for idx, (col_name, fig) in enumerate(charts):
                    with cols[idx % 2]:
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No numeric columns available for statistical analysis")
        
        with tab3:
            st.header("Attribute Data")
            
            st.subheader("Watershed Attributes Table")
            
            display_df = gdf.drop(columns=['geometry']) if 'geometry' in gdf.columns else gdf
            
            search_term = st.text_input("🔍 Search in table:", "")
            if search_term:
                mask = display_df.astype(str).apply(
                    lambda x: x.str.contains(search_term, case=False, na=False)
                ).any(axis=1)
                display_df = display_df[mask]
            
            st.dataframe(display_df, use_container_width=True, height=500)
            
            csv = display_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="watershed_data.csv",
                mime="text/csv"
            )
        
        with tab4:
            st.header("Dataset Metadata")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("General Information")
                st.write(f"**Number of Features:** {len(gdf)}")
                st.write(f"**Number of Attributes:** {len(gdf.columns) - 1}")
                st.write(f"**Coordinate System:** {gdf.crs if gdf.crs else 'Not defined'}")
                st.write(f"**Geometry Type:** {gdf.geometry.geom_type.iloc[0] if len(gdf) > 0 else 'N/A'}")
            
            with col2:
                st.subheader("Spatial Extent")
                bounds = gdf.total_bounds
                st.write(f"**Min X:** {bounds[0]:.6f}")
                st.write(f"**Min Y:** {bounds[1]:.6f}")
                st.write(f"**Max X:** {bounds[2]:.6f}")
                st.write(f"**Max Y:** {bounds[3]:.6f}")
            
            st.subheader("Attribute Schema")
            schema_data = []
            for col in gdf.columns:
                if col != 'geometry':
                    schema_data.append({
                        'Column Name': col,
                        'Data Type': str(gdf[col].dtype),
                        'Non-Null Count': gdf[col].count(),
                        'Null Count': gdf[col].isna().sum()
                    })
            
            schema_df = pd.DataFrame(schema_data)
            st.dataframe(schema_df, use_container_width=True)
    
    else:
        st.info("👈 Please upload a shapefile or provide a path to get started")
        
        st.markdown("""
        ### How to use this dashboard:
        
        1. **Upload your shapefile** using the sidebar file uploader
           - You need to upload all components: .shp, .shx, .dbf, and .prj files
        
        2. **Or provide a file path** if your shapefile is already on the system
        
        3. **Explore the data** through different tabs:
           - **Map**: Interactive visualization with multiple base layers
           - **Statistics**: Summary statistics and distribution charts
           - **Data Table**: Browse and search attribute data
           - **Metadata**: View dataset information and schema
        
        4. **Customize visualizations** using the sidebar options:
           - Color watersheds by attribute values
           - Filter data by numeric ranges
           - Choose different color schemes
        
        ### Features:
        - 🗺️ Interactive maps with multiple base layers
        - 📊 Statistical analysis and visualizations
        - 🔍 Search and filter capabilities
        - 📥 Export data to CSV
        - 📏 Measurement tools on map
        - 🎨 Choropleth mapping for numeric attributes
        """)

if __name__ == "__main__":
    main()
