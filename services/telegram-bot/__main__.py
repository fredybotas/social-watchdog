from lib_core.repositories import WatchableRepository
from lib_core.services import WatchableService, WatchableLimiter
from pymongo.mongo_client import MongoClient
from telegram_bot import Bot
from dotenv import load_dotenv

client = MongoClient("mongodb://watchdog:watchdog@localhost:27017/")
watchable_repository = WatchableRepository(client)
watchable_service = WatchableService(
    watchable_repository=watchable_repository,
    limiter=WatchableLimiter(watchable_repository),
)
if __name__ == "__main__":
    load_dotenv()
    bot = Bot(watchable_service)
    bot.run()
