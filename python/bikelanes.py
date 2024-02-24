import folium 
import geopandas as gpd 
import os 

# Get the current working directory
cwd = os.getcwd()

# Construct the path to the shapefile
shapefile_path = os.path.join(cwd, 'dependencies', 'bike_lanes.shp')

chicago_map = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

bike_lanes = gpd.read_file("../dependencies/bike_lanes.shp")

# Check the CRS of the GeoDataFrame
print(bike_lanes.crs)  # This should print out the CRS information

# If the CRS is not set, you can set it manually
bike_lanes.crs = "EPSG:4326"

# Reproject the geometries to EPSG:4326
bike_lanes = bike_lanes.to_crs("EPSG:4326")

folium.GeoJson(bike_lanes).add_to(chicago_map)

chicago_map.save("chicago_map_bike_lanes.html")
