import asyncio
from liblog import get_logger
from libcore.types import Watchable
from libcore.repositories import WatchableRepository

logger = get_logger(__name__)


class PeriodicSearchWorker:
    def __init__(self, loop: any, repository: WatchableRepository, every: int) -> None:
        self.period = every
        self.loop = loop
        self.repository = repository

        self.loop.create_task(self.start())

    async def start(self):
        while True:
            await self.work()
            await asyncio.sleep(self.period)

    async def work(self):
        for watchable in self.repository.get_all({}):
            try:
                await self._process_watchable(watchable)
            except Exception as e:
                logger.error(
                    "Couldn't process watchable: {}, error: {}".format(watchable, e)
                )

    @staticmethod
    def get_notification_hash(submission_id: str, user_id: str) -> str:
        return submission_id + user_id

    async def _process_watchable(self, watchable: Watchable):
        raise NotImplementedError()
