from beanie import Document
from typing import Dict, Any, Optional, List


class DBConversation(Document):
    id: str
    name: str
    params: Optional[Dict[str, Any]] = {}
    tokens: int = 0

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
