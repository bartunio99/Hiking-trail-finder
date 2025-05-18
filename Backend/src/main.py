from logging import DEBUG
import sys
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from endpoints import map

app = FastAPI()
app.include_router(map.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  #Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
def main(argv=sys.argv[1:]):
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=DEBUG)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()