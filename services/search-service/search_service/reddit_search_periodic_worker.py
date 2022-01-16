from libcore.repositories import WatchableRepository
from libcore.types import Watchable, WatchableNotification
from libmq import UniqueMessageQueueClient
from liblog import get_logger
from search_service import WatchableProcessor
from .periodic_worker import PeriodicSearchWorker
from .lemmatizer import Lemmatizer
from libcore.types import Submission
import asyncpraw

logger = get_logger(__name__)


class RedditSearchWorker(PeriodicSearchWorker):
    def __init__(
        self,
        loop: any,
        period: int,
        praw_client: asyncpraw.Reddit,
        repository: WatchableRepository,
        mq_client: UniqueMessageQueueClient[WatchableNotification],
        watchable_processor: WatchableProcessor,
        lemmatizer: Lemmatizer,
    ) -> None:
        super().__init__(loop, repository, period)
        self.praw_client = praw_client
        self.mq_client = mq_client
        self.watchable_processor = watchable_processor
        self.lemmatizer = lemmatizer

    async def _process_watchable(self, watchable: Watchable) -> None:
        watchable_terms = " ".join(self.lemmatizer.lemmatize(watchable.watch))
        subreddit = await self.praw_client.subreddit(watchable.subreddit)
        async for response in subreddit.search(
            watchable_terms, sort="new", time_filter="hour"
        ):
            submission = Submission(
                id=str(response.id),
                url=response.shortlink,
                created_timestamp=response.created_utc,
                title=response.title,
                text=response.selftext,
            )
            notification = self.watchable_processor.get_notification_if_appropriate(
                watchable, submission
            )
            if notification is None:
                continue
            self.mq_client.enqueue(
                notification,
                PeriodicSearchWorker.get_notification_hash(
                    submission.id, watchable.provider_user_id
                ),
            )
