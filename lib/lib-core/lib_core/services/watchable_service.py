from lib_core.repositories import WatchableRepository
from lib_core.types.watchable import Watchable
import uuid
from typing import List

MAX_WATCHABLE_COUNT_PER_USER = 5


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


class WatchableService:
    def __init__(
        self, watchable_repository: WatchableRepository, limiter: WatchableLimiter
    ) -> None:
        self.repository = watchable_repository
        self.limiter = limiter

    def add_watchable(
        self, provider_user_id: str, effective_chat_id: str, subreddit: str, watch: str
    ) -> None:
        if self.limiter.should_allow_create(provider_user_id=provider_user_id) is False:
            raise LimitExceededError()
        watchable = Watchable(
            id=uuid.uuid4(),
            provider_user_id=provider_user_id,
            effective_chat_id=effective_chat_id,
            subreddit=subreddit,
            watch=watch,
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
