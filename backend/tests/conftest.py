# conftest.py
import asyncio
import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.server.app import app
from app.server.models.conversations import DBConversation

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def db_client():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    yield client
    client.close()

@pytest.fixture(scope="session")
async def prepare_beanie(db_client, event_loop):
    await init_beanie(database=db_client.test_db, document_models=[DBConversation])
    yield
    await db_client.your_db_name.drop_collection("conversations")

@pytest.fixture(scope="module")
def client(prepare_beanie):
    with TestClient(app) as test_client:
        yield test_client
