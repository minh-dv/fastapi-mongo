from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.user import User
from config.config import settings


async def initiate_database():
    client = AsyncIOMotorClient(settings.DB_URL)
    await init_beanie(database=client.test,
                      document_models=[User])
