### loads trails from OpenStreetMap and stores them in MongoDB
import overpy
from pymongo import MongoClient
from geopy.geocoders import Nominatim
from motor.motor_asyncio import AsyncIOMotorClient

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

        
        for way in result.ways:
            trail = {
                "name": way.tags.get("name", "Unnamed Trail"),
                "sac_scale": way.tags.get("sac_scale"),
                "tags": way.tags,
                "nodes": [(node.lat, node.lon) for node in way.nodes],
            }
            trails.append(trail)

        valid_trails = [trail for trail in trails if trail.get("sac_scale") is not None]

        return valid_trails

    except Exception as e:
        print(f"Error: {e}")
        return []

def store_trails_in_mongodb(trails, name):
    # Connect to MongoDB (make sure MongoDB is running)
    client = MongoClient(HOST)
    db = client[DB_NAME]  # Use or create database 'trail_db'

    collection = db[name]  # Use or create collection with the name of the place
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
        return True
    except ValueError as e:
        return False
        print(f"Error: {e}")
        exit(1)




    

