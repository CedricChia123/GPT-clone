from typing import List
import uuid
from fastapi import APIRouter, Body, HTTPException, status
from ..schema.responses import (
    query_response,
    APIError,
)
from ..models.conversations import DBConversation
from ..schema.conversation_schema import (
    CreatedResponse,
    Prompt,
)
from ..config import get_openai_response

router = APIRouter()


@router.post(
    "",
    response_model=CreatedResponse,
    status_code=status.HTTP_201_CREATED,
    responses=query_response,
    summary="Creates a new Prompt query",
)
async def create_prompt(id: str, prompt: Prompt):
    """
    This action sends a new Prompt query to the LLM and returns its response. If any errors occur when sending the prompt to the LLM, then a 422 error should be raised.
    """
    conversation = await DBConversation.get(id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified resource not found.",
        )

    request_data = {"role": prompt.role.value, "content": prompt.content}

    try:
        response_data = get_openai_response(request_data, conversation.messages)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=APIError(
                code=422,
                message="Unable to create resource.",
            ).model_dump(),
        )

    try:
        conversation.messages.append(prompt)
        conversation.messages.append(response_data)
        prompt_token_count = len(prompt.content)
        response_token_count = len(response_data.content)
        conversation.tokens += prompt_token_count + response_token_count

        await conversation.save()

        return CreatedResponse(id=id)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=APIError(
                code=500,
                message="Internal Server Error.",
            ).model_dump(),
        )
