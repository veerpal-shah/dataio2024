import geopandas as gpd
import pandas as pd
import contextily as ctx
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString


# Step 1: Load your data
# Assuming 'year.csv' is your data file with bike station information
data = pd.read_csv('year.csv')

'''
# Convert DataFrame to GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.start_lng, data.start_lat))

# Set the coordinate reference system (CRS) to WGS84 (EPSG:4326) and then convert to Web Mercator (EPSG:3857) for contextily
gdf.crs = "EPSG:4326"
gdf = gdf.to_crs(epsg=3857)

# Step 2: Plotting
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color='red', markersize=1, alpha=0.1)

# Add OpenStreetMap basemap
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# Optional: Adjust the view to focus on the area of interest (e.g., Chicago area)
# These values might need adjustment to better frame your specific dataset
ax.set_xlim([-9780000, -9745000])
ax.set_ylim([5130000, 5165000])

# Remove x and y axis labels for a cleaner look
ax.set_axis_off()

plt.title('Bike Stations in Chicago')

# Save the plot as a PNG file
plt.savefig('Bike_Stations_in_Chicago.png', dpi=300)

# If you don't want the plot to display after saving, you can comment out plt.show()
# plt.show()

'''

data = data.dropna(subset=['start_lat', 'start_lng', 'end_lat', 'end_lng'])


members = data[data['member_casual'] == 'member']
casuals = data[data['member_casual'] == 'casual']

# Function to create a GeoDataFrame from bike routes
def create_routes_gdf(df):
    # Filter the DataFrame to remove rows with NaN values or identical start and end points
    filtered_df = df.dropna(subset=['start_lat', 'start_lng', 'end_lat', 'end_lng'])
    filtered_df = filtered_df[(filtered_df['start_lat'] != filtered_df['end_lat']) | (filtered_df['start_lng'] != filtered_df['end_lng'])]
    
    # Create LineString objects from start and end points
    geometry = [LineString([(x[0], x[1]), (x[2], x[3])]) for x in filtered_df[['start_lng', 'start_lat', 'end_lng', 'end_lat']].values]
    gdf = gpd.GeoDataFrame(filtered_df , geometry=geometry, crs="EPSG:4326")
    #gdf = gdf.to_crs(epsg=3857)
    return gdf
    

data = pd.read_csv('year.csv')
data = data.dropna(subset=['start_lat', 'start_lng', 'end_lat', 'end_lng'])

# Filter out rows where coordinates are outside the expected range for Chicago
data = data[
    (data['start_lat'].between(41.6, 42.1)) & 
    (data['start_lng'].between(-87.9, -87.5)) &
    (data['end_lat'].between(41.6, 42.1)) & 
    (data['end_lng'].between(-87.9, -87.5))
]


# Create subsets for members and casual riders
members = data[data['member_casual'] == 'member']
casuals = data[data['member_casual'] == 'casual']

# Ensure GeoDataFrames have their CRS set upon creation
gdf_members = create_routes_gdf(members)
gdf_casuals = create_routes_gdf(casuals)

# Now, the CRS conversion should work without raising an error
gdf_members = gdf_members.to_crs(epsg=3857)
gdf_casuals = gdf_casuals.to_crs(epsg=3857)

# Plotting
fig, ax = plt.subplots(figsize=(12, 12))
gdf_members.plot(ax=ax, linewidth=1, color='blue', label='Member')
gdf_casuals.plot(ax=ax, linewidth=1, color='red', label='Casual')

# Add base map
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# Set x and y limits to the extent of Chicago to avoid showing any outlying data
ax.set_xlim([-9780000, -9745000])
ax.set_ylim([5130000, 5165000])  

ax.set_axis_off()
plt.legend()
plt.title('Bike Routes: Members vs. Casual Riders')

# Save the plot
plt.savefig('bike_routes_member_vs_casual.png', dpi=300)