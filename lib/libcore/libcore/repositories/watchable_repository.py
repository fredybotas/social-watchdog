from typing import Dict
from .generic_repository import GenericMongoRepository, IGenericRepository
from libcore.types import Watchable
from pymongo import MongoClient
import bson


class IWatchableRepository(IGenericRepository):
    pass


class WatchableRepository(IWatchableRepository, GenericMongoRepository):
    TABLE_NAME = "watchables"

    def __init__(self, client: MongoClient) -> None:
        super().__init__(client, WatchableRepository.TABLE_NAME)

    def _serialize(self, element: Watchable) -> Dict[str, any]:
        return {
            "_id": bson.Binary.from_uuid(element.id),
            "provider_user_id": element.provider_user_id,
            "effective_chat_id": element.effective_chat_id,
            "subreddit": element.subreddit,
            "watch": element.watch,
        }

    def _deserialize(self, raw_data: Dict[str, any]) -> Watchable:
        return Watchable(
            id=raw_data["_id"].as_uuid(),
            provider_user_id=raw_data["provider_user_id"],
            effective_chat_id=raw_data["effective_chat_id"],
            subreddit=raw_data["subreddit"],
            watch=raw_data["watch"],
        )