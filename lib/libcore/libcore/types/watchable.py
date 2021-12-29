from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class Watchable:
    id: UUID
    provider_user_id: str
    effective_chat_id: str
    subreddit: Optional[str]
    watch: str
