from .periodic_worker import PeriodicWorkerBase
from libcore.repositories import WatchableRepository
from libcore.types import Watchable, WatchableNotification
from libmq import UniqueMessageQueueClient
import praw


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

    def work(self):
        for watchable in self.repository.get_all({}):
            self._process_watchable(watchable)

    def _process_watchable(self, watchable: Watchable):
        for submission in self.praw_client.subreddit(watchable.subreddit).search(
            watchable.watch, sort="new"
        ):
            notification = WatchableNotification(
                watchable_id=watchable.id, title=submission.title, url=submission.url
            )
            self.mq_client.enqueue(notification, submission.id)
            print("-----")
            print(submission.title)
            print(submission.name)
            print(submission.id)
