# 📸 Visual Guide - Watershed Dashboard

A step-by-step visual walkthrough of using the watershed dashboard.

## 🎬 Getting Started

### Step 1: Launch the Dashboard

```bash
streamlit run watershed_dashboard.py
```

Your browser will open to: `http://localhost:8501`

**What You'll See:**
```
┌─────────────────────────────────────────────────────────────┐
│  🌊 Watershed Analysis Dashboard                           │
│  Interactive visualization of watershed boundaries          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  👈 Please upload a shapefile or provide a path            │
│      to get started                                         │
│                                                             │
│  [How to use this dashboard section with instructions]      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Step 2: Sidebar - Load Your Data

**Left Sidebar:**
```
┌──────────────────────────┐
│ 📁 Data Input           │
├──────────────────────────┤
│                          │
│ Upload Shapefile         │
│ Components               │
│                          │
│ [Browse files...]        │
│ (.shp, .shx, .dbf, .prj) │
│                          │
│ ────── OR ──────         │
│                          │
│ Enter shapefile path:    │
│ [                      ] │
│ /path/to/watersheds.shp  │
│                          │
└──────────────────────────┘
```

**Two Ways to Load Data:**

#### Option A: Upload Files
1. Click "Browse files"
2. Select ALL files:
   - watershed.shp
   - watershed.shx
   - watershed.dbf
   - watershed.prj (recommended)
3. Files upload automatically
4. ✅ Success message appears

#### Option B: Enter Path
1. Type full path: `/home/user/data/watershed.shp`
2. Press Enter
3. ✅ Success message appears

### Step 3: After Loading - Dashboard Appears

**Main View - Four Tabs:**
```
┌─────────────────────────────────────────────────────────────┐
│  [🗺️ Map] [📊 Statistics] [📋 Data Table] [ℹ️ Metadata]   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Currently viewing: 🗺️ Map Tab                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🗺️ Map Tab Walkthrough

### What You See

```
┌─────────────────────────────────────────────────────────────┐
│  Watershed Map                                              │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┬──────────────┬────────────────┐             │
│  │ Total    │ Total Area   │ Avg Attribute  │             │
│  │ Water... │ 2,450.23 sq  │ 145.67        │             │
│  │ 15       │ units        │               │             │
│  └──────────┴──────────────┴────────────────┘             │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │              INTERACTIVE MAP                       │   │
│  │  ┌────────────┐                                   │   │
│  │  │ ☰ Layers   │  Watershed Boundaries            │   │
│  │  └────────────┘                                   │   │
│  │                                                     │   │
│  │     ╔══════════════════════════════╗              │   │
│  │     ║    Watershed Area A          ║              │   │
│  │     ║  [Blue polygon with borders] ║              │   │
│  │     ╚══════════════════════════════╝              │   │
│  │                                                     │   │
│  │        ╔═══════════════════╗                      │   │
│  │        ║  Watershed Area B ║                      │   │
│  │        ╚═══════════════════╝                      │   │
│  │                                                     │   │
│  │  [+ Zoom]  [- Zoom]  [⛶ Fullscreen]  [📏 Measure]│   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Interactive Features

#### 🖱️ Hover Over Watersheds
```
When you hover over a watershed:
┌────────────────────────┐
│ Watershed A1          │
│ ──────────────────────│
│ ID: WS_001            │
│ Area: 245.67 km²      │
│ Population: 12,450    │
│ Nitrogen: 3,245 kg/yr │
│ Forest: 45.2%         │
└────────────────────────┘
Tooltip appears with all attributes
```

#### 🗺️ Base Layer Selection
```
Click "☰ Layers" button to toggle:
┌────────────────────┐
│ ✓ OpenStreetMap   │  ← Currently active
│   Terrain          │
│   Light            │
│   Satellite        │
└────────────────────┘
```

#### 🔍 Zoom and Pan
- **Zoom**: Mouse wheel or [+] [-] buttons
- **Pan**: Click and drag map
- **Reset**: Double-click map

## 🎨 Sidebar - Visualization Options

### After Data Loads

```
┌──────────────────────────────────┐
│ 🎨 Visualization Options        │
├──────────────────────────────────┤
│                                  │
│ Color by attribute:              │
│ ┌──────────────────────────────┐│
│ │ None                    ▼   ││
│ └──────────────────────────────┘│
│                                  │
│ Options:                         │
│ • None (default blue)            │
│ • AREA_SQKM                     │
│ • NITROGEN_KG                   │
│ • POPULATION                    │
│ • FOREST_PCT                    │
│                                  │
├──────────────────────────────────┤
│ 📊 Filter Options               │
├──────────────────────────────────┤
│                                  │
│ Filter by attribute:             │
│ ┌──────────────────────────────┐│
│ │ None                    ▼   ││
│ └──────────────────────────────┘│
│                                  │
└──────────────────────────────────┘
```

### Example: Color by Area

**Before (No Coloring):**
```
All watersheds are light blue
```

**After Selecting "AREA_SQKM":**
```
┌──────────────────────────────────┐
│ Color by attribute:              │
│ ┌──────────────────────────────┐│
│ │ AREA_SQKM               ▼   ││
│ └──────────────────────────────┘│
│                                  │
│ Color scheme:                    │
│ ┌──────────────────────────────┐│
│ │ YlOrRd                  ▼   ││
│ └──────────────────────────────┘│
│                                  │
│ Options: Viridis, Blues,         │
│          RdYlGn, Plasma...       │
└──────────────────────────────────┘

Map updates with color gradient:
Yellow (small areas) → Orange → Red (large areas)

Legend appears on map:
┌──────────────┐
│ Area (km²)   │
│ 500 ■        │
│ 400 ■        │
│ 300 ■        │
│ 200 ■        │
│ 100 ■        │
└──────────────┘
```

### Example: Filter by Range

```
┌──────────────────────────────────┐
│ Filter by attribute:             │
│ ┌──────────────────────────────┐│
│ │ NITROGEN_KG             ▼   ││
│ └──────────────────────────────┘│
│                                  │
│ Select NITROGEN_KG range:        │
│ ├────○════════○────┤            │
│ 1000          8000 15000         │
│                                  │
│ Showing: 8 of 15 watersheds      │
└──────────────────────────────────┘

Map updates to show only watersheds
with nitrogen loads between 1000-8000
```

## 📊 Statistics Tab Walkthrough

```
┌─────────────────────────────────────────────────────────────┐
│  Statistical Analysis                                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Summary Statistics                                         │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Attribute  │ Mean   │ Median │ Std Dev│ Min │ Max  │  │
│  ├────────────┼────────┼────────┼────────┼─────┼──────┤  │
│  │ AREA_SQKM  │ 245.67 │ 238.45 │ 89.23  │ 50  │ 500  │  │
│  │ NITROGEN_KG│ 5245.3 │ 4892.1 │ 2341.8 │ 1000│15000 │  │
│  │ FOREST_PCT │ 45.2   │ 42.8   │ 18.9   │ 10  │ 80   │  │
│  │ POPULATION │ 15234  │ 12450  │ 9876   │ 1000│50000 │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  Distribution Charts                                        │
│  ┌─────────────────────────┐ ┌────────────────────────┐   │
│  │ Distribution of AREA_SQKM│ │ Distribution of       │   │
│  │       ▄                  │ │ NITROGEN_KG           │   │
│  │      ▄█▄                 │ │     ▄▄                │   │
│  │     ▄███▄                │ │    ████▄              │   │
│  │    ▄█████▄               │ │   ██████▄             │   │
│  │ ▄▄███████████▄           │ │ ▄████████▄            │   │
│  └─────────────────────────┘ └────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────┐ ┌────────────────────────┐   │
│  │ Distribution of         │ │ Distribution of        │   │
│  │ FOREST_PCT              │ │ POPULATION             │   │
│  │       ▄▄                │ │  ▄                     │   │
│  │      ████               │ │ ▄█▄                    │   │
│  │     ██████              │ │ ███▄                   │   │
│  │    ████████▄            │ │ █████▄                 │   │
│  │ ▄█████████████          │ │ ███████▄               │   │
│  └─────────────────────────┘ └────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**What You Can See:**
- Summary table with mean, median, std dev, min, max
- Histogram distributions for each numeric attribute
- Interactive charts (hover for exact values)
- Pattern identification

## 📋 Data Table Tab Walkthrough

```
┌─────────────────────────────────────────────────────────────┐
│  Attribute Data                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Watershed Attributes Table                                 │
│                                                             │
│  🔍 Search in table: [                                   ]  │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │ID    │Name      │Area  │Pop   │N(kg) │Forest%│... │   │
│  ├──────┼──────────┼──────┼──────┼──────┼───────┼────┤   │
│  │WS_001│Watershed A│245.67│12450 │3245  │45.2   │... │   │
│  │WS_002│Watershed B│198.34│8920  │2890  │52.1   │... │   │
│  │WS_003│Watershed C│367.89│25678 │6543  │38.9   │... │   │
│  │WS_004│Watershed D│156.23│6780  │2134  │61.3   │... │   │
│  │WS_005│Watershed E│289.45│18934 │4567  │42.7   │... │   │
│  │ ...  │  ...     │ ...  │ ... │ ...  │ ...   │... │   │
│  └────────────────────────────────────────────────────┘   │
│                                                             │
│  Showing 15 rows                                            │
│                                                             │
│  [📥 Download as CSV]                                       │
└─────────────────────────────────────────────────────────────┘
```

### Features:

#### 🔍 Search
```
Type "Watershed A" in search box
→ Table filters to show only matching rows
```

#### 📊 Sort Columns
```
Click column header to sort:
• Click "Area" → Sort by area (ascending)
• Click again → Sort descending
```

#### 📥 Export
```
Click "Download as CSV" button
→ Downloads: watershed_data.csv
→ Opens in Excel, R, Python, etc.
```

## ℹ️ Metadata Tab Walkthrough

```
┌─────────────────────────────────────────────────────────────┐
│  Dataset Metadata                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  General Information        │  Spatial Extent               │
│  ─────────────────────────  │  ──────────────────────────   │
│  Number of Features: 15     │  Min X: -96.500000            │
│  Number of Attributes: 23   │  Min Y: 40.000000             │
│  Coordinate System:         │  Max X: -94.000000            │
│    EPSG:4326 (WGS84)       │  Max Y: 41.500000             │
│  Geometry Type: Polygon     │                               │
│                                                             │
│  Attribute Schema                                           │
│  ┌────────────────────────────────────────────────────┐   │
│  │Column Name    │Data Type│Non-Null│Null Count│     │   │
│  ├───────────────┼─────────┼────────┼──────────┤     │   │
│  │WATERSHED_ID   │object   │15      │0         │     │   │
│  │NAME           │object   │15      │0         │     │   │
│  │AREA_SQKM      │float64  │15      │0         │     │   │
│  │PERIMETER_KM   │float64  │15      │0         │     │   │
│  │AVG_ELEVATION  │float64  │15      │0         │     │   │
│  │AVG_SLOPE      │float64  │15      │0         │     │   │
│  │NITROGEN_KG    │float64  │15      │0         │     │   │
│  │PHOSPHORUS_KG  │float64  │15      │0         │     │   │
│  │...            │...      │...     │...       │     │   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**What You Can See:**
- Total number of watersheds
- Coordinate system information
- Spatial extent (bounding box)
- Complete list of attributes with data types
- Data quality info (null counts)

## 🎯 Common Workflows

### Workflow 1: Explore Your Watershed Data

```
1. Load Data
   └→ Upload or enter path

2. View Map Tab
   └→ See watershed boundaries
   └→ Hover for details

3. Apply Colors
   └→ Select "Color by: NITROGEN_KG"
   └→ Choose color scheme: "YlOrRd"
   └→ See spatial patterns

4. Check Statistics
   └→ Go to Statistics Tab
   └→ Review summary stats
   └→ Examine distributions

5. Export Data
   └→ Go to Data Table Tab
   └→ Search/filter as needed
   └→ Download CSV
```

### Workflow 2: Identify High-Risk Areas

```
1. Load Data

2. Filter in Sidebar
   └→ "Filter by: NITROGEN_KG"
   └→ Adjust slider to high values
   └→ Map shows only high-nitrogen watersheds

3. Cross-Reference
   └→ Check Population in filtered areas
   └→ Check Urban % in filtered areas
   └→ Review in Data Table

4. Export Results
   └→ Download filtered CSV
   └→ Share with team
```

### Workflow 3: Compare Watersheds

```
1. Load Data

2. Color by Area
   └→ "Color by: AREA_SQKM"
   └→ Identify large vs small watersheds

3. Check Statistics
   └→ Compare distributions
   └→ Note correlations

4. Search Specific Ones
   └→ Go to Data Table
   └→ Search for specific IDs
   └→ Compare attributes
```

## 🎨 Color Scheme Examples

### For Water Quality Data
```
RdYlGn (Red-Yellow-Green)
Red = Poor Quality
Yellow = Moderate
Green = Good Quality
```

### For Nutrient Loads
```
YlOrRd (Yellow-Orange-Red)
Yellow = Low loads
Orange = Medium loads
Red = High loads
```

### For General Continuous Data
```
Viridis (Multi-hue)
Purple → Blue → Green → Yellow
- Colorblind friendly
- Perceptually uniform
```

## 💡 Pro Tips

### Tip 1: Layer Control
```
Click layer selector on map to:
- Switch base maps
- Find best background for your data
- Satellite view for land use context
- Terrain for topographic context
```

### Tip 2: Measurement Tool
```
Use measure tool to:
- Calculate distances between watersheds
- Measure watershed perimeters
- Verify area calculations
```

### Tip 3: Fullscreen Mode
```
Click fullscreen button:
- Better for presentations
- Easier to explore large datasets
- Press ESC to exit
```

### Tip 4: Combine Filters
```
Filter by multiple attributes:
1. Set nitrogen range filter
2. Color by forest percentage
3. See relationship between:
   - High nitrogen (filtered)
   - Low forest (red color)
```

### Tip 5: Export Strategy
```
Before exporting:
1. Apply all desired filters
2. Search for specific areas
3. Then download CSV
→ Only filtered data exports
```

## 🚀 Next Level Features

### Custom Analysis in Jupyter
```python
# Load your data
import geopandas as gpd
gdf = gpd.read_file('sample_data/watersheds.shp')

# Calculate custom metrics
gdf['n_yield'] = gdf['NITROGEN_KG'] / gdf['AREA_SQKM']

# Save back
gdf.to_file('watersheds_analyzed.shp')

# Load in dashboard to visualize new metrics!
```

### Share Your Dashboard
```
Deploy to Streamlit Cloud:
1. Push to GitHub
2. Go to streamlit.io/cloud
3. Connect repo
4. Share link with team!
```

## 📱 Dashboard on Mobile

The dashboard works on tablets and phones:
- Responsive design
- Touch-friendly controls
- Pinch to zoom on maps
- Swipe to pan

Best experience: **Tablet in landscape mode**

## 🎓 Learn More

- **QUICKSTART.md** - Setup in 5 minutes
- **WATERSHED_README.md** - Full documentation
- **watershed_tutorial.ipynb** - Hands-on tutorial
- **PROJECT_SUMMARY.md** - Technical overview

---

**🎉 You're ready to explore your watershed data!**

Start with the quick start guide, load your data, and discover insights in your watersheds.
