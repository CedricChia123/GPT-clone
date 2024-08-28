import motor.motor_asyncio
from beanie import init_beanie
from .models.conversations import DBConversation

client = None

async def init_db():
    global client
    mongo_url = "mongodb://localhost:27017/"
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
    
    await init_beanie(database=client.db_name, document_models=[DBConversation])

async def off_db():
    global client
    if client is not None:
        client.close()
        client = None