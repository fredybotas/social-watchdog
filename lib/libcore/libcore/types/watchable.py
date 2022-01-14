from dataclasses import dataclass
from typing import Optional
from datetime import date
from enum import Enum


class WatchableProcessorType(Enum):
    STRICT = "strict"
    DEFAULT = "default"


@dataclass
class Watchable:
    id: str
    provider_user_id: str
    effective_chat_id: str
    subreddit: Optional[str]
    watch: str
    processor_type: WatchableProcessorType
    created_at: date
