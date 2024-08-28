from typing import List
import uuid
from fastapi import APIRouter, Body, HTTPException, status
from ..schema.responses import (
    conversation_response,
    get_conversation_response,
    put_conversation_response,
    get_one_conversation_response,
    delete_conversation_response,
    APIError,
)
from ..models.conversations import DBConversation
from ..schema.conversation_schema import (
    ConversationPOST,
    Conversation,
    ConversationPUT,
    CreatedResponse,
    ConversationFull,
)

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
            status_code=status.HTTP_500_BAD_REQUEST,
            detail=APIError(
                code=500,
                message="Internal server error",
                details={"error": str(e)},
            ).model_dump(),
        )


@router.put(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=put_conversation_response,
    summary="Updates the LLM properties of a Conversations",
)
async def update_conversation(id: str, update_data: ConversationPUT = Body(...)):
    """
    Allows the user to customise parameters and properties of a Conversation, thereby customising their experience.
    """
    conversation = await DBConversation.get(id)

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=APIError(
                code=404,
                message="Specified resource(s) not found.",
                request=update_data.model_dump(),
                details={"error": f"{id} not found"},
            ).model_dump(),
        )

    else:
        try:
            update_data_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_data_dict.items():
                setattr(conversation, key, value)
            await conversation.save()
            return "Successfully updated specified resource"
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=APIError(
                    code=500,
                    message="Internal Server Error.",
                    request=update_data.model_dump(),
                    details={"error": str(e)},
                ).model_dump(),
            )


@router.get(
    "/{id}",
    response_model=ConversationFull,
    status_code=status.HTTP_200_OK,
    responses=get_one_conversation_response,
    summary="Retrieves the Conversation History",
)
async def get_conversation(id: str):
    """
    Retrieves the entire conversation history with the LLM
    """
    conversation = await DBConversation.get(id)

    if conversation:
        return conversation

    elif not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=APIError(
                code=404,
                message="Specified resource(s) not found.",
                request=f"GET conversation {id} not found",
                details={"error": f"{id} not found"},
            ).model_dump(),
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=APIError(
                code=500,
                message="Internal Server Error.",
                request=f"GET conversation {id} server error",
                details={"error": str(e)},
            ).model_dump(),
        )


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=delete_conversation_response,
    summary="Deletes the Conversation",
)
async def delete_conversation(id: str):
    """
    Deletes the entire conversation history with the LLM Model
    """
    conversation = await DBConversation.get(id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=APIError(
                code=404,
                message="Specified resource not found.",
                request=f"DELETE conversation {id} not found",
                details={"error": f"{id} not found"},
            ).model_dump(),
        )

    try:
        await DBConversation.delete(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=APIError(
                code=500,
                message="Internal Server Error.",
                request=f"DELETE conversation {id} server error",
                details={"error": str(e)},
            ).model_dump(),
        )
