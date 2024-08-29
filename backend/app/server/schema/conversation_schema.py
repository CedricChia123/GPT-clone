from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional


class Params(BaseModel):
    class Config:
        extra = "allow"


class ConversationPOST(BaseModel):
    name: str
    params: Params = Field(default_factory=Params)

    class Config:
        extra = "allow"
        schema_extra = {"description": "POST request for creating a new Conversation"}


class CreatedResponse(BaseModel):
    id: str

    class Config:
        extra = "allow"


class Conversation(BaseModel):
    id: str
    name: str
    params: Params
    tokens: int

    class Config:
        extra = "allow"


class ConversationPUT(BaseModel):
    name: Optional[str] = None
    params: Optional[Params] = None


class QueryRoleType(Enum):
    system = "system"
    user = "user"
    assistant = "assistant"
    function = "function"


class Prompt(BaseModel):
    role: QueryRoleType = "user"
    content: str


class ConversationFull(Conversation):
    messages: List[Prompt]

    class Config:
        extra = "allow"
