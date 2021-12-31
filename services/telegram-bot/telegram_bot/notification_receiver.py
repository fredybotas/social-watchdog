from libmq import UniqueMessageQueueClient
from .bot import Bot
from libcore.types import WatchableNotification
from libcore.repositories import WatchableRepository


class NotificationReceiver:
    def __init__(
        self,
        bot: Bot,
        mq_client: UniqueMessageQueueClient,
        watchable_repository: WatchableRepository,
    ) -> None:
        self.bot = bot
        self.mq_client = mq_client
        self.watchable_repository = watchable_repository

    def start(self):
        self.mq_client.listen(self._process_notification)

    def _process_notification(self, notification: WatchableNotification):
        watchable = self.watchable_repository.get_one({"id": notification.watchable_id})
        if watchable is not None:
            self.bot.send_message(
                watchable.effective_chat_id,
                text="New match:\ntitle: {}\nurl: {})".format(
                    notification.title, notification.url
                ),
            )
