from telegram_bot import WatchableService, WatchableLimiter

from libcore.repositories import WatchableRepository
from libmq import UniqueMessageQueueClient, WATCHABLE_NOTIFICATION_QUEUE_KEY
from pymongo.mongo_client import MongoClient
from telegram_bot import Bot
from telegram_bot import NotificationReceiver
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../../.env")

client = MongoClient(os.getenv("DB_URL"))
watchable_repository = WatchableRepository(client)
watchable_service = WatchableService(
    watchable_repository=watchable_repository,
    limiter=WatchableLimiter(watchable_repository),
)
bot = Bot(watchable_service)
mq_client = UniqueMessageQueueClient(WATCHABLE_NOTIFICATION_QUEUE_KEY)
notification_receiver = NotificationReceiver(bot, mq_client, watchable_repository)

if __name__ == "__main__":
    bot.run()
    notification_receiver.start()
