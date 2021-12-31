from libcore.workers import RedditSearchWorker
from libcore.repositories import WatchableRepository
from libcore.types import WatchableNotification
from libmq import UniqueMessageQueueClient, WATCHABLE_NOTIFICATION_QUEUE_KEY
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
import praw

load_dotenv(dotenv_path="../../.env")

praw_client = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    redirect_uri=os.getenv("REDDIT_REDIRECT_URI"),
    user_agent="Trender by u/fredybotas",
)
client = MongoClient(os.getenv("DB_URL"))
repository = WatchableRepository(client)
mq_client = UniqueMessageQueueClient[WatchableNotification](
    WATCHABLE_NOTIFICATION_QUEUE_KEY
)

worker = RedditSearchWorker(5, praw_client, repository, mq_client)

if __name__ == "__main__":
    worker.start()
