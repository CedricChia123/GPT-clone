from beanie import Document
from datetime import datetime
from typing import Dict, Any, Optional

class DBConversation(Document):
    id: str
    name: str
    params: Optional[Dict[str, Any]] = {}
    created_at: datetime = datetime.now() 

    class Settings:
        name = "conversations"
        allow_extra_fields = True

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"
        
