from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Params(BaseModel):
    class Config:
        extra = "allow" 

class ConversationPOST(BaseModel):
    name: str
    params: Params = Field(default_factory=Params)
    
    class Config:
        extra = "allow"
        schema_extra = {
            "description": "POST request for creating a new Conversation"
        }

class CreatedResponse(BaseModel):
    id: str
