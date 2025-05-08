#map-related endpoints
from fastapi import APIRouter
import overpy

router = APIRouter()

@router.get("/map/city/{city_name}")
async def return_city(city_name:str):
    return city_name