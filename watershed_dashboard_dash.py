"""
Watershed Dashboard using Plotly Dash
Alternative implementation with Dash framework
"""

import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import pandas as pd
import json
from pathlib import Path

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

SHAPEFILE_PATH = None
gdf_global = None

def load_shapefile(filepath):
    """Load shapefile and return GeoDataFrame"""
    try:
        gdf = gpd.read_file(filepath)
        if gdf.crs is None:
            gdf = gdf.set_crs("EPSG:4326")
        else:
            gdf = gdf.to_crs("EPSG:4326")
        return gdf
    except Exception as e:
        print(f"Error loading shapefile: {str(e)}")
        return None

def create_choropleth_map(gdf, color_column=None):
    """Create choropleth map using Plotly"""
    
    gdf_copy = gdf.copy()
    gdf_copy['id'] = range(len(gdf_copy))
    
    if color_column and color_column in gdf_copy.columns:
        if pd.api.types.is_numeric_dtype(gdf_copy[color_column]):
            color_data = gdf_copy[color_column]
        else:
            color_data = None
    else:
        color_data = None
    
    fig = go.Figure()
    
    for idx, row in gdf_copy.iterrows():
        geom = row.geometry
        
        if geom.geom_type == 'Polygon':
            coords = list(geom.exterior.coords)
            lons = [coord[0] for coord in coords]
            lats = [coord[1] for coord in coords]
            
            hover_text = f"ID: {idx}<br>"
            for col in gdf_copy.columns:
                if col not in ['geometry', 'id']:
                    hover_text += f"{col}: {row[col]}<br>"
            
            color = 'lightblue' if color_data is None else None
            
            fig.add_trace(go.Scattermapbox(
                lon=lons,
                lat=lats,
                mode='lines',
                fill='toself',
                fillcolor='rgba(135, 206, 250, 0.5)',
                line=dict(width=2, color='darkblue'),
                hovertext=hover_text,
                hoverinfo='text',
                name=f'Watershed {idx}'
            ))
        
        elif geom.geom_type == 'MultiPolygon':
            for poly in geom.geoms:
                coords = list(poly.exterior.coords)
                lons = [coord[0] for coord in coords]
                lats = [coord[1] for coord in coords]
                
                hover_text = f"ID: {idx}<br>"
                for col in gdf_copy.columns:
                    if col not in ['geometry', 'id']:
                        hover_text += f"{col}: {row[col]}<br>"
                
                fig.add_trace(go.Scattermapbox(
                    lon=lons,
                    lat=lats,
                    mode='lines',
                    fill='toself',
                    fillcolor='rgba(135, 206, 250, 0.5)',
                    line=dict(width=2, color='darkblue'),
                    hovertext=hover_text,
                    hoverinfo='text',
                    name=f'Watershed {idx}',
                    showlegend=False
                ))
    
    center_lat = gdf_copy.geometry.centroid.y.mean()
    center_lon = gdf_copy.geometry.centroid.x.mean()
    
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=center_lat, lon=center_lon),
            zoom=8
        ),
        showlegend=False,
        height=600,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    
    return fig

def create_app_layout():
    """Create the dashboard layout"""
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("🌊 Watershed Analysis Dashboard", className="text-center mb-4"),
                html.P("Interactive visualization of watershed boundaries and attributes", 
                       className="text-center text-muted")
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📁 Load Shapefile"),
                    dbc.CardBody([
                        dbc.Input(
                            id='shapefile-path-input',
                            placeholder='Enter path to shapefile (.shp)',
                            type='text',
                            className='mb-2'
                        ),
                        dbc.Button('Load Data', id='load-button', color='primary', className='w-100')
                    ])
                ])
            ], width=12)
        ], className='mb-4'),
        
        html.Div(id='status-message'),
        
        html.Div(id='dashboard-content')
        
    ], fluid=True)

app.layout = create_app_layout()

@app.callback(
    [Output('status-message', 'children'),
     Output('dashboard-content', 'children')],
    [Input('load-button', 'n_clicks')],
    [State('shapefile-path-input', 'value')]
)
def load_and_display_data(n_clicks, shapefile_path):
    """Load shapefile and create dashboard"""
    
    if n_clicks is None or not shapefile_path:
        return dbc.Alert("Please enter a shapefile path and click 'Load Data'", color="info"), None
    
    if not Path(shapefile_path).exists():
        return dbc.Alert(f"File not found: {shapefile_path}", color="danger"), None
    
    gdf = load_shapefile(shapefile_path)
    
    if gdf is None:
        return dbc.Alert("Error loading shapefile", color="danger"), None
    
    global gdf_global
    gdf_global = gdf
    
    numeric_columns = gdf.select_dtypes(include=['number']).columns.tolist()
    
    map_fig = create_choropleth_map(gdf)
    
    stats_cards = []
    if numeric_columns:
        for col in numeric_columns[:3]:
            card = dbc.Card([
                dbc.CardBody([
                    html.H4(col, className="card-title"),
                    html.H2(f"{gdf[col].mean():.2f}", className="text-primary"),
                    html.P(f"Min: {gdf[col].min():.2f} | Max: {gdf[col].max():.2f}", 
                          className="card-text")
                ])
            ])
            stats_cards.append(dbc.Col(card, width=4))
    
    distribution_figs = []
    if numeric_columns:
        for col in numeric_columns[:4]:
            fig = px.histogram(gdf, x=col, title=f'Distribution of {col}', nbins=30)
            fig.update_layout(height=300)
            distribution_figs.append(dbc.Col(dcc.Graph(figure=fig), width=6))
    
    display_df = gdf.drop(columns=['geometry']) if 'geometry' in gdf.columns else gdf
    
    table_component = dash_table.DataTable(
        id='data-table',
        columns=[{"name": col, "id": col} for col in display_df.columns],
        data=display_df.to_dict('records'),
        page_size=20,
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'minWidth': '100px'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        filter_action='native',
        sort_action='native',
        export_format='csv'
    )
    
    dashboard = html.Div([
        dbc.Tabs([
            dbc.Tab([
                dbc.Row([
                    dbc.Col(stats_cards, width=12) if stats_cards else None
                ], className='mb-4'),
                
                dbc.Row([
                    dbc.Col([
                        html.H4("Watershed Boundaries Map"),
                        dcc.Graph(figure=map_fig, id='watershed-map')
                    ])
                ])
            ], label="🗺️ Map"),
            
            dbc.Tab([
                html.H4("Statistical Analysis", className='mb-4'),
                dbc.Row(distribution_figs) if distribution_figs else html.P("No numeric columns available")
            ], label="📊 Statistics"),
            
            dbc.Tab([
                html.H4("Attribute Data", className='mb-4'),
                table_component
            ], label="📋 Data Table"),
            
            dbc.Tab([
                html.H4("Dataset Metadata", className='mb-4'),
                dbc.Row([
                    dbc.Col([
                        html.H5("General Information"),
                        html.P(f"Number of Features: {len(gdf)}"),
                        html.P(f"Number of Attributes: {len(gdf.columns) - 1}"),
                        html.P(f"Coordinate System: {gdf.crs}"),
                        html.P(f"Geometry Type: {gdf.geometry.geom_type.iloc[0] if len(gdf) > 0 else 'N/A'}")
                    ], width=6),
                    dbc.Col([
                        html.H5("Spatial Extent"),
                        html.P(f"Min X: {gdf.total_bounds[0]:.6f}"),
                        html.P(f"Min Y: {gdf.total_bounds[1]:.6f}"),
                        html.P(f"Max X: {gdf.total_bounds[2]:.6f}"),
                        html.P(f"Max Y: {gdf.total_bounds[3]:.6f}")
                    ], width=6)
                ])
            ], label="ℹ️ Metadata")
        ])
    ])
    
    success_msg = dbc.Alert(
        f"✅ Successfully loaded {len(gdf)} watershed features", 
        color="success", 
        dismissable=True
    )
    
    return success_msg, dashboard

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
