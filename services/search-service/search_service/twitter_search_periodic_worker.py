from libcore.repositories import WatchableRepository
from libcore.types import Watchable, WatchableNotification, Submission
from libmq import UniqueMessageQueueClient
from liblog import get_logger
from search_service import WatchableProcessor
from .periodic_worker import PeriodicSearchWorker
from .lemmatizer import Lemmatizer
from datetime import datetime, timedelta
import tweepy

logger = get_logger(__name__)

NOT_RETWEET_QUERY = "-is:retweet"


class TwitterSearchWorker(PeriodicSearchWorker):
    def __init__(
        self,
        loop: any,
        period: int,
        tweepy: tweepy.Client,
        repository: WatchableRepository,
        mq_client: UniqueMessageQueueClient[WatchableNotification],
        watchable_processor: WatchableProcessor,
        lemmatizer: Lemmatizer,
    ) -> None:
        super().__init__(loop, repository, period)
        self.tweepy = tweepy
        self.mq_client = mq_client
        self.watchable_processor = watchable_processor
        self.lemmatizer = lemmatizer

    def _get_twitter_query(self, watchable: Watchable) -> str:
        lemmas = self.lemmatizer.lemmatize(watchable.watch)
        terms = watchable.watch.split(" ")
        if len(lemmas) != len(terms):
            return watchable.watch + " " + NOT_RETWEET_QUERY
        return " ".join(
            ["({} OR {})".format(le, te) for le, te in zip(lemmas, terms)]
            + [NOT_RETWEET_QUERY]
        )

    async def _process_watchable(self, watchable: Watchable) -> None:
        response = self.tweepy.search_recent_tweets(
            query=self._get_twitter_query(watchable),
            start_time=datetime.utcnow() - timedelta(hours=1),
            end_time=datetime.utcnow() - timedelta(seconds=15),
            max_results=100,
        )
        if response.data is None:
            return
        for tweet in response.data:
            submission = Submission(
                id=str(tweet.id),
                url="twitter.com/twitter/status/" + str(tweet.id),
                created_timestamp=datetime.utcnow().timestamp(),  # TODO: Currently we don't receive tweet timestamp. Try to fix this.
                title="Tweet",
                text=tweet.text,
            )
            notification = self.watchable_processor.get_notification_if_appropriate(
                watchable, submission
            )
            if notification is None:
                continue
            self.mq_client.enqueue(
                notification,
                PeriodicSearchWorker.get_notification_hash(
                    submission.id, watchable.provider_user_id
                ),
            )
