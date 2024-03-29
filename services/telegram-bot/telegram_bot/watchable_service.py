from libcore.repositories import WatchableRepository
from libcore.types import Watchable, WatchableProcessorType
import uuid
from typing import List
from datetime import datetime

MAX_WATCHABLE_COUNT_PER_USER = 10


class WatchableLimiter:
    def __init__(
        self, repository: WatchableRepository, limit: int = MAX_WATCHABLE_COUNT_PER_USER
    ) -> None:
        self.repository = repository
        self.limit = limit

    def should_allow_create(self, provider_user_id: str) -> bool:
        if (
            len(self.repository.get_all({"provider_user_id": provider_user_id}))
            < self.limit
        ):
            return True
        return False


class LimitExceededError(Exception):
    pass


class NotFoundError(Exception):
    pass


class InvalidProcessingTypeError(Exception):
    pass


class WatchableService:
    def __init__(
        self, watchable_repository: WatchableRepository, limiter: WatchableLimiter
    ) -> None:
        self.repository = watchable_repository
        self.limiter = limiter

    def add_watchable(
        self,
        provider_user_id: str,
        effective_chat_id: str,
        subreddit: str,
        processing_type: str,
        watch: str,
    ) -> None:
        if self.limiter.should_allow_create(provider_user_id=provider_user_id) is False:
            raise LimitExceededError()
        # TODO: move validation to upper layer
        try:
            _ = WatchableProcessorType(processing_type)
        except Exception:
            raise InvalidProcessingTypeError()
        watchable = Watchable(
            id=str(uuid.uuid4()),
            provider_user_id=provider_user_id,
            effective_chat_id=effective_chat_id,
            subreddit=subreddit,
            processor_type=WatchableProcessorType(processing_type),
            watch=watch,
            created_at=datetime.utcnow(),
        )
        self.repository.insert_one(watchable)

    def get_all_watchables_for_user(self, provider_user_id: str) -> List[Watchable]:
        return self.repository.get_all({"provider_user_id": provider_user_id})

    def remove_watchable(self, provider_user_id: str, id: str) -> None:
        if (
            self.repository.get_one({"provider_user_id": provider_user_id, "id": id})
            is None
        ):
            raise NotFoundError()
        self.repository.remove(id)
