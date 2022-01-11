import redis
import os
from typing import TypeVar
from liblog import get_logger
from typing import Generic
import threading
import pickle
import time

logger = get_logger(__name__)
T = TypeVar("T")


WATCHABLE_NOTIFICATION_QUEUE_KEY = "watchable_notification_queue"


class UniqueMessageQueueClient(Generic[T]):
    def __init__(self, queue_key: str) -> None:
        self.queue_key = queue_key
        self.set_key = queue_key + "_set"
        self.host = os.getenv("REDIS_HOST")
        self.port = os.getenv("REDIS_PORT")
        self.listening = False
        self._reconnect()

    def _reconnect(self):
        self.redis = redis.Redis(host=self.host, port=self.port, db=0)

    def enqueue(self, element: T, unique_identifier: str):
        try:
            if self.redis.sismember(self.set_key, unique_identifier):
                return
            pipeline = self.redis.pipeline(transaction=True)
            pipeline.lpush(self.queue_key, pickle.dumps(element))
            pipeline.sadd(self.set_key, unique_identifier)
            pipeline.execute()
        except redis.ConnectionError:
            logger.error("Redis connection lost during enqueue")

    def listen(self, process_fn: any):
        self.listening = True
        self.listen_thread = threading.Thread(
            target=self._listen_loop, args=(process_fn,)
        )
        self.listen_thread.start()

    def _listen_loop(self, process_fn: any):
        while self.listening is True:
            try:
                element = pickle.loads(self.redis.brpop(self.queue_key)[1])
                process_fn(element)
            except redis.ConnectionError:
                logger.error("Redis connection lost during receiving")
                time.sleep(1)

    def stop(self):
        if self.listening is False:
            return
        self.listening = False
        self.listen_thread.join()
