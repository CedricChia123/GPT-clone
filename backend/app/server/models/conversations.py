from beanie import Document
from typing import Dict, Any, Optional, List
from ..schema.conversation_schema import Prompt


class DBConversation(Document):
    id: str
    name: str
    params: Optional[Dict[str, Any]] = {}
    tokens: int = 0
    messages: List[Prompt] = []

    class Settings:
        name = "conversations"
        allow_extra_fields = True

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    @classmethod
    async def get_all_conversations(cls) -> List["DBConversation"]:
        """
        Fetches all conversation records from the database.
        """
        return await cls.find_all().to_list()

    @classmethod
    async def get(cls, conversation_id: str) -> Optional["DBConversation"]:
        """
        Fetches a single conversation record from the database by its ID.
        """
        return await cls.find_one(cls.id == conversation_id)

    @classmethod
    async def delete(cls, conversation_id: str) -> bool:
        """
        Deletes a single conversation record from the database by its ID.
        """
        await cls.find_one(cls.id == conversation_id).delete()
