from libcore.repositories import WatchableRepository
from libcore.types import Watchable, WatchableNotification
from libmq import UniqueMessageQueueClient
from liblog import get_logger
from search_service import WatchableProcessor
from search_service.text_matchers import DefaultMatcher, StrictMatcher
from .periodic_worker import PeriodicWorkerBase

import praw

logger = get_logger(__name__)


class RedditSearchWorker(PeriodicWorkerBase):
    def __init__(
        self,
        period: int,
        praw_client: praw.Reddit,
        repository: WatchableRepository,
        mq_client: UniqueMessageQueueClient[WatchableNotification],
    ) -> None:
        super().__init__(period)
        self.repository = repository
        self.praw_client = praw_client
        self.mq_client = mq_client
        self.watchable_processor = WatchableProcessor(
            strict_matcher=StrictMatcher(), default_matcher=DefaultMatcher()
        )

    def work(self):
        for watchable in self.repository.get_all({}):
            try:
                self._process_watchable(watchable)
            except Exception as e:
                logger.error(
                    "Couldn't process watchable: {}, error: {}".format(watchable, e)
                )

    @staticmethod
    def get_notification_hash(submission_id: str, user_id: str) -> str:
        return submission_id + user_id

    def _process_watchable(self, watchable: Watchable):
        for submission in self.praw_client.subreddit(watchable.subreddit).search(
            watchable.watch, sort="new"
        ):
            notification = self.watchable_processor.get_notification_if_appropriate(
                watchable, submission
            )
            if notification is None:
                continue
            self.mq_client.enqueue(
                notification,
                RedditSearchWorker.get_notification_hash(
                    submission.id, watchable.provider_user_id
                ),
            )
