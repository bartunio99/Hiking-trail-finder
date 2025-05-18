#map-related endpoints

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from db import database as db
from visualization import visualization
from trails import recommendation
import os

class Place(BaseModel):
    name: str
    radius: float


router = APIRouter()

#gets trails from vicinity and stores them in mongoDB database
@router.post("/map/places/")
async def load_trails(place:Place):
    try:
        # Load trails from the specified location and radius
        result = db.load_local_trails(place.name, place.radius)
        if result:
            return {"message": f"Trails loaded successfully for {place.name}."}
        else:
            return {"message": f"No trails found for {place.name}."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
#returns only trails of given difficulty - very slow :<
@router.get("/map/places/difficulty/")
async def get_trails_by_difficulty(name: str, difficulty: str):
    try:
        # Get trails from the database
        trails = db.return_hikes_by_difficulty(name, difficulty)
        if trails:
            return {"trails": trails}
        else:
            return {"message": f"No trails found for {name} with difficulty {difficulty}."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
#return map of trails - html
@router.post("/map/places/maps/")
async def gen_map(place: Place):
    place_name = place.name+ "-" + str(place.radius)
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))       # this file's folder
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))  # up one level
    dir = os.path.join(PROJECT_ROOT, "maps")

    for file in os.listdir(dir):
        if file.startswith(place_name) and file.endswith(".html"):
            return FileResponse(os.path.join(dir, file))
    
    #in case map not generated
    database, client = db.init_connection()
    collection = database[place_name]
    visualization.visualize_trails(collection)
    return FileResponse(os.path.join(dir, place_name + ".html"))

@router.delete("/map/places/{place_name}/")
async def delete_trails(place_name: str):
    try:
        # Get trails from the database
        db.delete_collection(place_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/map/places/{place_name}/")
async def find_trails(place_name: str):
    try:
        # Get trails from the database
        hikes = db.find_collection(place_name)
        return hikes
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/map/places/")
async def get_places():
    try:
        # Get trails from the database
        database, _ = db.init_connection()
        collection_names = db.return_collection_names(database)
        return {"places": collection_names}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/map/recommendation/")
async def get_recommendation(difficulty: int, place_name: str, length: float):
    try:
        # Get trails from the database
        if place_name:
            recommendations = recommendation.recommend_trails(difficulty, length, place_name)
            return {"recommendations": recommendations}
        else:
            return {"message": f"No trails found for {place_name} with difficulty {difficulty} and length {length}."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
