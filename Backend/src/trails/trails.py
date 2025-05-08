### loads trails from OpenStreetMap and stores them in MongoDB
import overpy
from pymongo import MongoClient
from geopy.geocoders import Nominatim

DB_NAME = 'trail_db'
HOST = "mongodb://localhost:27017/"

def get_place_coordinates(place_name):
    geolocator = Nominatim(user_agent="trail_locator")
    location = geolocator.geocode(place_name)

    if location:
        print(f"{place_name} coordinates: ({location.latitude}, {location.longitude})")
        return location.latitude, location.longitude
    else:
        raise ValueError(f"Could not find coordinates for {place_name}")    

def get_trails_nearby(lat, lon, radius_km=5):
    api = overpy.Overpass()

    # Convert radius to degrees (approximate: 1 degree ≈ 111 km)
    radius_deg = radius_km / 111.0
    radius_m = radius_km * 1000.0

    min_lat = lat - radius_deg
    max_lat = lat + radius_deg
    min_lon = lon - radius_deg
    max_lon = lon + radius_deg

    query = f"""
        [out:json][timeout:60];
        (
        // Get paths/footways with mountain-related tags
        way(around:{radius_m},{lat},{lon})["highway"~"path|footway"]["sac_scale"];
        way(around:{radius_m},{lat},{lon})["highway"~"path|footway"]["mtb:scale"];
        way(around:{radius_m},{lat},{lon})["highway"~"path|footway"]["incline"];
        way(around:{radius_m},{lat},{lon})["highway"~"path|footway"]["surface"~"unpaved|ground|rock|gravel"];
        );
        // Filter out short trails (less than 4 nodes)
        way._(if:count_tags() >= 4);
        out body;
        >;
        out skel qt;
        """


    try:
        result = api.query(query)
        trails = []

        #valid_ways = [way for way in result.ways if len(way.nodes) > 3]


        for way in result.ways:
            trail = {
                "name": way.tags.get("name", "Unnamed Trail"),
                "sac_scale": way.tags.get("sac_scale", "N/A"),
                "tags": way.tags,
                "nodes": [(node.lat, node.lon) for node in way.nodes],
            }
            trails.append(trail)

        return trails

    except Exception as e:
        print(f"Error: {e}")
        return []

def store_trails_in_mongodb(trails, name):
    # Connect to MongoDB (make sure MongoDB is running)
    client = MongoClient(HOST)
    db = client[DB_NAME]  # Use or create database 'trail_db'
    collection_name = 'trails_' + name
    collection = db[collection_name]  # Use or create collection 'trails'

    # Insert trail data into MongoDB
    if trails:
        #clean decimal to float type (coordinates)
        for trail in trails:
            trail['nodes'] = [(float(lat), float(lon)) for lat, lon in trail['nodes']]
        # Insert the trails into the collection
        collection.insert_many(trails)
        print(f"Stored {len(trails)} trails in MongoDB.")
    else:
        print("No trails to store.")

#radius in km
def load_local_trails(location_name:str, radius:float):
    try:
        latitude, longitude = get_place_coordinates(location_name)
        trails = get_trails_nearby(latitude,longitude,radius)

        store_trails_in_mongodb(trails, location_name)
    except ValueError as e:
        print(e)
        exit(1)




    

