import geopandas as gpd
import osmnx as ox
import neatnet



dist = 2200

from types import SimpleNamespace

# Define all cities in one namespace
cities = SimpleNamespace(
    barc=SimpleNamespace(name="Barcelona", coord=(41.381426, 2.173053), crs=25831),
    ath=SimpleNamespace(name="Athens", coord=(37.989702027509686, 23.738142824327344), crs=2100),
    tyo=SimpleNamespace(name="Tokyo", coord=(35.702950, 139.769753), crs=3099),
    lbrgh=SimpleNamespace(name="Loughborough", coord=(52.767225, -1.220030), crs=27700),
    mk=SimpleNamespace(name="Milton Keynes", coord=(52.0406, -0.7594), crs=27700),
    ldn=SimpleNamespace(name="London - Camden", coord=(51.543001, -0.183654), crs=27700)  # NEW
)

# Choose the city prefix you want to analyze
selected_city_key = 'barc'  # Switch to 'ath' or 'barc' etc.

# Create a reference to the selected city
city = getattr(cities, selected_city_key)



# GET OSM DATA
center_point = city.coord
custom_filter = (
    '["highway"~"motorway|trunk|primary|secondary|tertiary|footway|pedestrian|path|steps"]'
)
custom_filter1 = '["highway"~"motorway|trunk|primary|secondary|tertiary|unclassified|residential|service"]'	

osm_graph=ox.graph.graph_from_point(
    center_point, 
    dist, 
    dist_type='bbox', 
    network_type= 'drive', # "all_public", "all", "bike", "drive", "drive_service", "walk"
    simplify=True, 
    retain_all=True, 
    truncate_by_edge=True, 
    custom_filter=custom_filter1)

print(f"Downloaded street network for {center_point}")

# you already built `osm_graph` above
G = osm_graph

# Convert to GeoDataFrames
nodes_gdf, edges_gdf = ox.graph_to_gdfs(G)

# Ensure WGS84 (GeoJSON expects lon/lat)
nodes_gdf = nodes_gdf.to_crs(epsg=4326)
edges_gdf = edges_gdf.to_crs(epsg=4326)

# Write out as GeoJSON (separate files: points + lines)
nodes_gdf.to_file("street_nodes.geojson", driver="GeoJSON")
edges_gdf.to_file("street_edges.geojson", driver="GeoJSON")

print("Saved GeoJSON: street_nodes.geojson and street_edges.geojson")



