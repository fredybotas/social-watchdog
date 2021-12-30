from .periodic_worker import PeriodicWorkerBase
from libcore.repositories import WatchableRepository
from libcore.types import Watchable
import schedule
import praw


class RedditSearchWorker(PeriodicWorkerBase):
    def __init__(
        self,
        scheduler: schedule.Scheduler,
        praw_client: praw.Reddit,
        repository: WatchableRepository,
    ) -> None:
        super().__init__(scheduler)
        self.repository = repository
        self.praw_client = praw_client

    def work(self):
        for watchable in self.repository.get_all({}):
            self._process_watchable(watchable)

    def _process_watchable(self, watchable: Watchable):
        for submission in self.praw_client.subreddit(watchable.subreddit).search(
            watchable.watch, sort="new"
        ):
            print("-----")
            print(submission.title)
            print(submission.name)
