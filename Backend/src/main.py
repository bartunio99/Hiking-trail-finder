from logging import DEBUG
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from db.database import init_connection

from endpoints import map

app = FastAPI()
app.include_router(map.router)

class Item(BaseModel):
    text:str
    is_done:bool=False

items = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items")
def create_item(item:Item):
    items.append(item)
    return items

@app.get("/items",response_model=list[Item])
def list_items(limit: int = 10):
    return items[0:limit]


@app.get("/items/{item_id}",response_model=Item)
def get_item(item_id:int) -> Item:
    if item_id < len(items):
        item = items[item_id]
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found!")
    
def main(argv=sys.argv[1:]):
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=3001, reload=DEBUG)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()