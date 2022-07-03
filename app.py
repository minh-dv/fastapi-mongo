from fastapi import FastAPI
from db.database import initiate_database
from api.api import api_router

app = FastAPI()


@app.on_event("startup")
async def start_database():
    await initiate_database()


app.include_router(api_router, prefix="/v1")
