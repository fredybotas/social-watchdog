from search_service import (
    Lemmatizer,
    RedditSearchWorker,
    WatchableProcessor,
    DefaultMatcher,
    StrictMatcher,
    TwitterSearchWorker,
)
from libcore.repositories import WatchableRepository
from libcore.types import WatchableNotification
from libmq import UniqueMessageQueueClient, WATCHABLE_NOTIFICATION_QUEUE_KEY
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
import asyncpraw
import asyncio
import tweepy

load_dotenv(dotenv_path="../../.env")


loop = asyncio.new_event_loop()
period = 30 * 60  # in seconds


async def main():
    global reddit_W
    praw_client = asyncpraw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        redirect_uri=os.getenv("REDDIT_REDIRECT_URI"),
        user_agent="Trender by u/fredybotas",
    )
    tweepy_client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))
    mongo_client = MongoClient(os.getenv("DB_URL"))
    repository = WatchableRepository(mongo_client)
    mq_client = UniqueMessageQueueClient[WatchableNotification](
        WATCHABLE_NOTIFICATION_QUEUE_KEY
    )
    watchable_processor = WatchableProcessor(
        strict_matcher=StrictMatcher(), default_matcher=DefaultMatcher()
    )
    lemmatizer = Lemmatizer()
    _ = RedditSearchWorker(
        loop,
        period,
        praw_client,
        repository,
        mq_client,
        watchable_processor,
        lemmatizer,
    )
    _ = TwitterSearchWorker(
        loop,
        period,
        tweepy_client,
        repository,
        mq_client,
        watchable_processor,
        lemmatizer,
    )


if __name__ == "__main__":
    try:
        loop.create_task(main())
        loop.run_forever()
    except asyncio.CancelledError:
        pass
