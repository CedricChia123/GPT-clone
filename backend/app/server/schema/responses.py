from pydantic import BaseModel, Field
from typing import Any, Optional


class APIError(BaseModel):
    code: int = Field(..., description="API error code associated with the error")
    message: str = Field(..., description="Error message associated with the error")
    request: Optional[Any] = Field(
        None, description="Request details associated with the error"
    )
    details: Optional[Any] = Field(
        None, description="Other details associated with the error"
    )


conversation_response = {
    201: {
        "description": "Successfully created resource with ID",
        "content": {
            "application/json": {
                "example": {"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}
            }
        },
    },
    400: {
        "description": "Invalid parameter(s) provided.",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "message": "Invalid parameters provided",
                }
            }
        },
        "model": APIError,
    },
    500: {
        "description": "Invalid parameter(s) provided.",
        "content": {
            "application/json": {
                "example": {
                    "code": 500,
                    "message": "Internal Server Error",
                }
            }
        },
        "model": APIError,
    },
}

get_conversation_response = {
    200: {
        "description": "Successfully retrieved a list of Conversations.",
        "content": {
            "application/json": {
                "example": {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": "string",
                    "params": {"additionalProp1": {}},
                    "tokens": 0,
                    "additionalProp1": {},
                }
            }
        },
    },
    500: {
        "description": "Invalid parameter(s) provided.",
        "content": {
            "application/json": {
                "example": {"code": 500, "message": "Internal Server Error"}
            }
        },
        "model": APIError,
    },
}
