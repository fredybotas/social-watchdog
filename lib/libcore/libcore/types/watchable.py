from dataclasses import dataclass
from typing import Optional


@dataclass
class Watchable:
    id: str
    provider_user_id: str
    effective_chat_id: str
    subreddit: Optional[str]
    watch: str
