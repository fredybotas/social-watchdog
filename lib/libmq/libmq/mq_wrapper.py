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


class UniqueMessageQueueClient(Generic[T]):
    def __init__(
        self,
        queue_key: str,
        host: str = os.getenv("REDIS_HOST"),
        port: int = os.getenv("REDIS_PORT"),
    ) -> None:
        self.queue_key = queue_key
        self.set_key = queue_key + "_set"
        self.host = host
        self.port = port
        self.listening = False
        self._reconnect()

    def _reconnect(self):
        self.redis = redis.Redis(host=self.host, port=self.port, db=0)
        self.redis.expire(self.set_key, 60 * 60 * 24)

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
