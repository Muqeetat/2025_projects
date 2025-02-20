import uvicorn
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException
from datetime import datetime
from enum import Enum
from app.routers import user, pickuprequest, complaint, auth



# Create the FastAPI app
app = FastAPI()



# the routers defined in the routers folder
app.include_router(complaint.router)
app.include_router(pickuprequest.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)