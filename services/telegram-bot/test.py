from lib_core.repositories import WatchableRepository
from lib_core.types import Watchable

from pymongo import MongoClient
import uuid

db_string = "mongodb://watchdog:watchdog@localhost:27017/"
client = MongoClient(db_string)
repo = WatchableRepository(client)
watchable = Watchable(id=uuid.uuid4(), subreddit="aaaa", watch="sss")
repo.insert_one(watchable)
print(repo.get_all({"id": watchable.id, "subreddit": "aaaa"}))
