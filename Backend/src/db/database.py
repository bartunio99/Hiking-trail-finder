### handles database communication
from pymongo import MongoClient
from trails import trails
from haversine import haversine, Unit

HOST = trails.HOST
DB_NAME = trails.DB_NAME

#initializes connection to MongoDB database
def init_connection():
    client = MongoClient(HOST)
    db = client[DB_NAME] 
    return db

#loads trails from vicinity to mongoDB database
def load_local_trails(location_name, radius):
    result = trails.load_local_trails(location_name, radius)
    return result

#debug purposes
def print_collections(db):
    # Print all collections in the database
    print("Collections in the database:")
    for collection_name in db.list_collection_names():
        print(f"- {collection_name}")

#returns collection names - names of looked places
def return_collection_names(db):
    # Return all collections in the database
    return db.list_collection_names()

def return_collection(db,collection_name):
    # Return a specific collection from the database
    return db[collection_name]

def append_difficulty(difficulty):
    # Append difficulty to the collection
    if difficulty == 1:
        return "hiking"
    elif difficulty == 2:
        return "mountain_hiking"
    elif difficulty == 3:
        return "demanding_mountain_hiking"
    elif difficulty == 4:
        return "alpine_hiking"
    elif difficulty == 5:
        return "demanding_alpine_hiking"
    elif difficulty == 6:
        return "difficult_alpine_hiking"

#dificulty by scale from 1 to 6 in chosen collection
def return_hikes_by_difficulty(db, colection_name, difficulty):
    collection = db[colection_name]
    difficulty = append_difficulty(difficulty)
    hikes = []

    for hike in collection.find({"sac_scale": difficulty}):
        hikes.append({
            "name": hike["name"],
            "sac_scale": hike["sac_scale"],
            "tags": hike["tags"],
            "nodes": hike["nodes"]
        })
    return hikes

#calculate estimated distance of the hike (not taking the elevation into account)
def calculate_route_distance(hike):
    distance = 0
    # Calculate the length of the hike using haversine formula
    for i in range(len(hike["nodes"]) - 1):
        distance += haversine(tuple(hike["nodes"][i]), tuple(hike["nodes"][i+1]))

    return distance

def add_place(db, place_name, collection_name="places"):
    collection = db[collection_name]
    x = collection.insert_one({"name": place_name})
    


def return_hikes_by_length(db, colection_name, length):
    collection = db[colection_name]
    hikes = []

    
    
if __name__ == "__main__":
    db = init_connection()
    load_local_trails("Teide", 10)
    print(return_collection_names(db))
    # hike = return_hikes_by_difficulty(db, "trails_Fogo", 2)[0]
    # print(calculate_route_distance(hike))
    #add_place(db, "Fogo")
