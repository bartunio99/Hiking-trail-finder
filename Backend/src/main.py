from logging import DEBUG
import sys
from fastapi import FastAPI, HTTPException
import uvicorn
from db.database import init_connection

from endpoints import map

app = FastAPI()
app.include_router(map.router)
    
def main(argv=sys.argv[1:]):
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=3001, reload=DEBUG)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()