from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class Watchable:
    id: UUID
    subreddit: Optional[str]
    watch: str
