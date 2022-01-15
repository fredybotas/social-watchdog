from typing import Dict
from .generic_repository import GenericMongoRepository, IGenericRepository
from libcore.types import Watchable, WatchableProcessorType
from pymongo import MongoClient
import bson
from uuid import UUID


class IWatchableRepository(IGenericRepository):
    pass


class WatchableRepository(IWatchableRepository, GenericMongoRepository):
    TABLE_NAME = "watchables"

    def __init__(self, client: MongoClient) -> None:
        super().__init__(client, WatchableRepository.TABLE_NAME)

    def _serialize(self, element: Watchable) -> Dict[str, any]:
        return {
            "_id": bson.Binary.from_uuid(UUID(element.id)),
            "provider_user_id": element.provider_user_id,
            "effective_chat_id": element.effective_chat_id,
            "subreddit": element.subreddit,
            "watch": element.watch,
            "processor_type": element.processor_type.value,
            "created_at": element.created_at,
        }

    def _deserialize(self, raw_data: Dict[str, any]) -> Watchable:
        return Watchable(
            id=str(raw_data["_id"].as_uuid()),
            provider_user_id=str(raw_data["provider_user_id"]),
            effective_chat_id=str(raw_data["effective_chat_id"]),
            subreddit=raw_data["subreddit"],
            watch=raw_data["watch"],
            processor_type=WatchableProcessorType(raw_data["processor_type"]),
            created_at=raw_data["created_at"],
        )
