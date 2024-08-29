from fastapi import APIRouter, HTTPException, status
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
        data = get_openai_response(request_data, conversation.messages, conversation.params)
        response_data = data["response"]
        tokens_used = data["tokens_used"]

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
        conversation.tokens = tokens_used

        await conversation.save()

        return CreatedResponse(id=id, response=response_data.content)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=APIError(
                code=500,
                message="Internal Server Error.",
                details=f"{e}",
                request="Server Error"
            ).model_dump(),
        )
