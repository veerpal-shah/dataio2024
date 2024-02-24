import geopandas as gpd
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx

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
    return gdf

# Convert to GeoDataFrame
gdf_members = create_points_gdf(members)
gdf_casuals = create_points_gdf(casuals)

# Convert to Web Mercator
gdf_members = gdf_members.to_crs(epsg=3857)
gdf_casuals = gdf_casuals.to_crs(epsg=3857)

# Extract x and y coordinates for KDE plot
members_points = gdf_members.geometry.apply(lambda p: (p.x, p.y)).tolist()
casuals_points = gdf_casuals.geometry.apply(lambda p: (p.x, p.y)).tolist()
members_x, members_y = zip(*members_points)
casuals_x, casuals_y = zip(*casuals_points)

# Create KDE plots
fig, ax = plt.subplots(figsize=(12, 12))
sns.kdeplot(x=members_x, y=members_y, levels=30, color='blue', alpha=0.5, label='Member', ax=ax, bw_adjust=1)
sns.kdeplot(x=casuals_x, y=casuals_y, levels=30, color='red', alpha=0.5, label='Casual', ax=ax, bw_adjust=1)

# Add base map
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)

# Set x and y limits to the extent of Chicago
ax.set_xlim([-9780000, -9745000])
ax.set_ylim([5130000, 5165000]) 

# Remove axis labels for a cleaner look
ax.set_axis_off()
plt.legend()
plt.title('Bike Trip Density: Members vs. Casual Riders')

# Save the plot
plt.savefig('bike_trip_density_member_vs_casual.png', dpi=200)
