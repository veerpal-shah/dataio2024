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

# Adding two markers for Most used station and least used station

most_used_arr = [[[lat, long], "Station #", "# rented"]]


for tup in most_used_arr:
    str = "Station {}, {} bikes rented".format(tup[2], tup[3])
    folium.Marker(location=tup[0], popup=str, icon=folium.Icon(color="blue")).add_to(chicago_map)
    
least_used_arr = [[[lat, long], "Station #", "# rented"]]

for tup in least_used_arr:
    str = "Station {}, {} bikes rented".format(tup[2], tup[3])
    folium.Marker(location=tup[0], popup=str, icon=folium.Icon(color="red")).add_to(chicago_map)


most_used_location = [41.89228, -87.61204]
least_used_location = [41.79, -87.65]

most_used_label = "Station 13022, 215,724,292,269 bikes rented"
least_used_label = "Station 769, 214,371 bikes rented"

# Add the markers to the map

folium.Marker(location=least_used_location, popup=least_used_label, icon=folium.Icon(color="red")).add_to(chicago_map)

chicago_map.save("chicago_map_bike_lanes.html")
