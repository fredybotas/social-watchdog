from libcore.repositories import WatchableRepository
from libcore.services import WatchableService, WatchableLimiter
from pymongo.mongo_client import MongoClient
from telegram_bot import Bot
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../../.env")

client = MongoClient(os.getenv("DB_URL"))
watchable_repository = WatchableRepository(client)
watchable_service = WatchableService(
    watchable_repository=watchable_repository,
    limiter=WatchableLimiter(watchable_repository),
)
if __name__ == "__main__":
    bot = Bot(watchable_service)
    bot.run()
