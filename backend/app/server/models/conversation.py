from beanie import Document
from pydantic import BaseModel
from datetime import datetime

class Conversation(Document):
    queries: list[str]
    responses: list[str]
