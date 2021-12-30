from libcore.repositories import WatchableRepository
from libcore.types import Watchable

from liblog import get_logger
from pymongo import MongoClient
import uuid

db_string = "mongodb://watchdog:watchdog@localhost:27017/"
client = MongoClient(db_string)
repo = WatchableRepository(client)
watchable = Watchable(
    id=uuid.uuid4(),
    provider_user_id="a",
    effective_chat_id="b",
    subreddit="aaaa",
    watch="sss",
)
repo.insert_one(watchable)
print(repo.get_all({"id": str(watchable.id), "subreddit": "aaaa"}))
