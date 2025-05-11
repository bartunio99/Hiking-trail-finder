#map-related endpoints
from typing import Any
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from db import database as db

#for id validation
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
        
class Place(BaseModel):
    name: str
    radius: float

# class Route(BaseModel):
#     id: PyObjectId = Field(alias="_id")
#     name: str
#     sac_scale: str
#     tags: dict
#     nodes: list

#     class Config:
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}

router = APIRouter()

#gets trails from vicinity and stores them in mongoDB database
@router.put("/map/places/{place_name}")
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
    
# @router.get("/map/places/{place_id}")
# async def get_trail(place_id: str):
