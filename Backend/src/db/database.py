### handles database communication
from pymongo import MongoClient
from trails import trails

HOST = trails.HOST
DB_NAME = trails.DB_NAME

#initializes connection to MongoDB database
def init_connection():
    client = MongoClient(HOST)
    db = client[DB_NAME] 
    return db, client

#loads trails from vicinity to mongoDB database
def load_local_trails(location_name, radius):
    result = trails.load_local_trails(location_name, radius)
    return result

#debug purposes
def print_collections(db):
    for collection_name in db.list_collection_names():
        print(f"- {collection_name}")

#returns collection names - names of looked places
def return_collection_names(db):
    return db.list_collection_names()

def return_collection(db,collection_name):
    # Return a specific collection from the database
    return db[collection_name]

def append_difficulty(difficulty):
    mapping = {
        1: "hiking",
        2: "mountain_hiking",
        3: "demanding_mountain_hiking",
        4: "alpine_hiking",
        5: "demanding_alpine_hiking",
        6: "difficult_alpine_hiking"
    }
    if difficulty in mapping:
        return mapping[difficulty]
    else:
        raise ValueError(f"Invalid difficulty level: {difficulty}")
    
#dificulty by scale from 1 to 6 in chosen collection
def return_hikes_by_difficulty(colection_name, difficulty):
    db, client = init_connection()
    collection = db[colection_name]
    difficulty = append_difficulty(int(difficulty))

    hikes = []

    for hike in collection.find({"sac_scale": difficulty}):
        hikes.append({
            "name": hike.get("name"),
            "sac_scale": hike.get("sac_scale"),
            "tags": hike.get("tags"),
            "nodes": hike.get("nodes"),
            "length": hike.get("length"),
        })

    client.close()
    return hikes



def find_collection(collection_name):
    db, client = init_connection()
    # Find trails in the collection that match the location name
    if collection_name in db.list_collection_names():
        collection = db[collection_name]
        hikes = []
        for hike in collection.find():
            hikes.append({
                "name": hike.get("name"),
                "sac_scale": hike.get("sac_scale"),
                "tags": hike.get("tags"),
                "nodes": hike.get("nodes"),
                "length": hike.get("length"),
            })
        client.close()
        return hikes
    else:
        client.close()
        return{f"Collection '{collection_name}' does not exist."}
    

def delete_collection(collection_name):
    # Delete a collection from the database
    db, client = init_connection()

    if collection_name in db.list_collection_names():
        db.drop_collection(collection_name)
        client.close()
        return {f"Collection '{collection_name}' deleted."}
    else:
        client.close()
        return{f"Collection '{collection_name}' does not exist."}
    
    

def return_hikes_by_length(db, colection_name, length):
    collection = db[colection_name]
    hikes = []

    
if __name__ == "__main__":
    print("x")
    db, _ = init_connection()
    print_collections(db)
