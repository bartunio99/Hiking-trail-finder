import folium
from pymongo.collection import Collection
from trails import trails
from db import database as db
from pymongo import MongoClient
import os
from config import MAPS_DIR

difficulty_colors = {
    "hiking": "blue",
    "mountain_hiking": "green",
    "demanding_mountain_hiking": "yellow",
    "alpine_hiking": "orange",
    "demanding_alpine_hiking": "red",
    "difficult_alpine_hiking": "black"
}


#visualize all trails in collection
def visualize_trails(collection : Collection):
    name = collection.name
    location = trails.get_place_coordinates(name)

    # Create a map centered at the average coordinates of the trails
    m = folium.Map(location=location, zoom_start=12)
    
    # Add trails to the map
    for trail in collection.find():
        color = difficulty_colors.get(trail["sac_scale"], "gray")  
        nodes = trail.get("nodes", [])
        if nodes:
            folium.PolyLine(locations=nodes, color=color, weight=2.5, opacity=1).add_to(m)
            folium.PolyLine(locations=nodes, color=color).add_to(m)

    output_path = os.path.join(MAPS_DIR, f"{name}.html")
    m.save(output_path)

def visualize_trail(trail):
    # Create a map centered at the average coordinates of the trail
    m = folium.Map(location=trail["nodes"][0], zoom_start=12)
    
    # Add the trail to the map
    color = difficulty_colors.get(trail["sac_scale"], "gray")  
    folium.PolyLine(locations=trail["nodes"], color=color, weight=2.5, opacity=1).add_to(m)

    output_path = os.path.join(MAPS_DIR, "user_track.html")
    m.save(output_path)


if __name__ == "__main__":
    # Example usage
    client = MongoClient(db.HOST)
    database = client[db.DB_NAME]
    collection = database["Teide"]
    
    # Visualize trails in the collection
    visualize_trails(collection)
    
