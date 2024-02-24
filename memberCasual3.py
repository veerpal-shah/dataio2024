import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx

# Define a function to add a basemap
def add_basemap(ax, source=ctx.providers.CartoDB.Positron):
    ctx.add_basemap(ax, source=source)
    xmin, xmax, ymin, ymax = ax.axis()
    basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    # reset the axis to the bounding box of the data
    ax.axis((xmin, xmax, ymin, ymax))

# Load data and filter
data = pd.read_csv('July.csv')
data = data.dropna(subset=['start_lat', 'start_lng', 'end_lat', 'end_lng'])
data = data[
    (data['start_lat'].between(41.6, 42.1)) & 
    (data['start_lng'].between(-87.9, -87.5)) &
    (data['end_lat'].between(41.6, 42.1)) & 
    (data['end_lng'].between(-87.9, -87.5))
]

# Separate members and casual riders
members = data[data['member_casual'] == 'member']
casuals = data[data['member_casual'] == 'casual']

# Function to convert to GeoDataFrame
def create_points_gdf(df):
    geometry = [Point(xy) for xy in zip(df.start_lng, df.start_lat)]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    gdf = gdf.to_crs(epsg=3857)  # Convert to Web Mercator for contextily
    return gdf

# Convert to GeoDataFrame
gdf_members = create_points_gdf(members)
gdf_casuals = create_points_gdf(casuals)

# Plotting - create a subplot for members and casuals
fig, axs = plt.subplots(1, 2, figsize=(20, 10), sharex=True, sharey=True)

# Plot hexbin for members
hb_members = axs[0].hexbin(gdf_members.geometry.x, gdf_members.geometry.y, gridsize=120, cmap='Blues', alpha=0.6, mincnt=1)
add_basemap(axs[0])
axs[0].set_title('Members')

# Plot hexbin for casuals
hb_casuals = axs[1].hexbin(gdf_casuals.geometry.x, gdf_casuals.geometry.y, gridsize=120, cmap='Reds', alpha=0.6, mincnt=1)
add_basemap(axs[1])
axs[1].set_title('Casual Riders')

# Sync axis limits across subplots
axs[0].set_xlim([-9780000, -9745000])
axs[0].set_ylim([5130000, 5165000])

# Remove axis labels for a cleaner look
for ax in axs:
    ax.set_axis_off()

plt.suptitle('Bike Trip Density: Members vs. Casual Riders')

# Save the plot
plt.savefig('bike_trip_density_member_vs_casual_hexbin.png', dpi=200)

plt.show()
