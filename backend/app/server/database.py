import motor.motor_asyncio
from .models.conversation import Conversation
from beanie import init_beanie

async def init_db():
    mongo_url = "mongodb://localhost:27017/"
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)

    await init_beanie(database=client.db_name, document_models=[Conversation])