### handles database communication
from pymongo import MongoClient
from trails import trails
import haversine

HOST = trails.HOST
DB_NAME = trails.DB_NAME

#initializes connection to MongoDB database
def init_connection():
    client = MongoClient(HOST)
    db = client[DB_NAME] 
    return db

#loads trails from vicinity to mongoDB database
def load_local_trails(location_name, radius):
    trails.load_local_trails(location_name, radius)

#debug purposes
def print_collections(db):
    # Print all collections in the database
    print("Collections in the database:")
    for collection_name in db.list_collection_names():
        print(f"- {collection_name}")

#returns collection name
def return_collection_names(db):
    # Return all collections in the database
    return db.list_collection_names()

if __name__ == "__main__":
    db = init_connection()
    #load_local_trails("Ślęża", 10)
    print(return_collection_names(db))
