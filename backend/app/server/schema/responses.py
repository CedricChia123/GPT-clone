from pydantic import BaseModel, Field
from typing import Any, Optional

class APIError(BaseModel):
    code: int = Field(..., description="API error code associated with the error")
    message: str = Field(..., description="Error message associated with the error")
    request: Optional[Any] = Field(None, description="Request details associated with the error")
    details: Optional[Any] = Field(None, description="Other details associated with the error")

conversation_response = {
    201: {"description": "Conversation created successfully."},
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
        "model": APIError
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
        "model": APIError
    }
}