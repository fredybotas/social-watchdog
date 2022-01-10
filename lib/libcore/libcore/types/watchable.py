from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Watchable:
    id: str
    provider_user_id: str
    effective_chat_id: str
    subreddit: Optional[str]
    watch: str
    created_at: date
