### loads trails from OpenStreetMap and stores them in MongoDB
import overpy
from pymongo import MongoClient
from geopy.geocoders import Nominatim
import math
import haversine
from motor.motor_asyncio import AsyncIOMotorClient

DB_NAME = 'trail_db'
HOST = "mongodb://mongodb:27017"


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
    radius_m = radius_km * 1000.0
    delta_lat = radius_km / 111   #one degree of latitude is approximately 111 km
    delta_lon = radius_km / (111 * math.cos(math.radians(lat)))

    south = lat - delta_lat
    north = lat + delta_lat
    west = lon - delta_lon
    east = lon + delta_lon

    query = f"""
        [out:json][timeout:60];
        (
        way["highway"~"path|footway"]["sac_scale"]({south},{west},{north},{east});
        way["highway"~"path|footway"]["mtb:scale"]({south},{west},{north},{east});
        way["highway"~"path|footway"]["incline"]({south},{west},{north},{east});
        way["highway"~"path|footway"]["surface"~"unpaved|ground|rock|gravel"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;
        """

    try:
        result = api.query(query)
        trails = []

        for way in result.ways:
            nodes = [(node.lat, node.lon) for node in way.nodes]
            trail = {
                "name": way.tags.get("name", "Unnamed Trail"),
                "sac_scale": way.tags.get("sac_scale"),
                "tags": way.tags,
                "nodes": nodes,
                "length": calculate_route_distance({"nodes": nodes})
            }
            trails.append(trail)

        valid_trails = [trail for trail in trails if trail.get("sac_scale") is not None]

        return valid_trails

    except Exception as e:
        print(f"Error: {e}")
        return []
    
#calculate estimated distance of the hike (not taking the elevation into account)
def calculate_route_distance(hike):
    distance = 0
    # Calculate the length of the hike using haversine formula
    for i in range(len(hike["nodes"]) - 1):
        distance += haversine.haversine(tuple(hike["nodes"][i]), tuple(hike["nodes"][i+1]))

    return distance

def store_trails_in_mongodb(trails, name):
    # Connect to MongoDB
    client = MongoClient(HOST)
    db = client[DB_NAME]  

    collection = db[name]  # Use or create collection with the name of the place
    # Insert trail data 
    if trails:
        #clean decimal to float type (coordinates)
        for trail in trails:
            trail['nodes'] = [(float(lat), float(lon)) for lat, lon in trail['nodes']]
        # Insert the trails into the collection
        collection.insert_many(trails)
        print(f"Stored {len(trails)} trails in MongoDB.")
    else:
        print("No trails to store.")

def load_local_trails(location_name:str, radius:float):
    try:
        latitude, longitude = get_place_coordinates(location_name)
        trails = get_trails_nearby(latitude,longitude,radius)

        store_trails_in_mongodb(trails, location_name +"-" + str(radius))
        return True
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
        
