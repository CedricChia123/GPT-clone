from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from typing import List

from ..models.conversation import Conversation

router = APIRouter()

@router.post("/", response_description="Conversation added to the database")
async def add_conversation(conversation: Conversation) -> dict:
    await conversation.create()
    return {"message": "Conversation added successfully"}