from typing import List
import uuid
from fastapi import APIRouter, HTTPException, status
from ..schema.responses import (
    conversation_response,
    get_conversation_response,
    APIError,
)
from ..models.conversations import DBConversation
from ..schema.conversation_schema import ConversationPOST, Conversation, CreatedResponse

router = APIRouter()


@router.post(
    "",
    response_model=CreatedResponse,
    status_code=status.HTTP_201_CREATED,
    responses=conversation_response,
    summary="Creates a new Conversation with an LLM model",
)
async def create_conversation(conversation_request: ConversationPOST):
    """
    A Conversation describes a series of interactions with an LLM model.
    It also contains the properties that will be used to send individual queries to the LLM.
    Chat queries will be anonymised and logged for audit purposes.
    """
    try:
        conversation_id = str(uuid.uuid4())
        new_conversation = DBConversation(
            id=conversation_id, **conversation_request.model_dump()
        )
        await new_conversation.create()
        return CreatedResponse(id=conversation_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=APIError(
                code=500,
                message="Internal Server Error.",
                request=conversation_request.model_dump(),
                details={"error": str(e)},
            ).model_dump(),
        )


@router.get(
    "",
    response_model=List[Conversation],
    status_code=status.HTTP_200_OK,
    responses=get_conversation_response,
    summary="Retrieve a user's Conversation",
)
async def get_conversations():
    """
    Retrieves all the conversations that a user has created, the conversation history is not provided here.
    """
    try:
        conversations = await DBConversation.get_all_conversations()
        return conversations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
