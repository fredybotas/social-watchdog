from typing import Dict
from .generic_repository import GenericMongoRepository, IGenericRepository
from ..types import Watchable
from pymongo import MongoClient
import bson


class IWatchableRepository(IGenericRepository):
    pass


class WatchableRepository(IWatchableRepository, GenericMongoRepository):
    TABLE_NAME = "watchables"

    def __init__(self, client: MongoClient) -> None:
        super().__init__(client, WatchableRepository.TABLE_NAME)

    def _serialize(self, element: Watchable) -> Dict:
        return {
            "_id": bson.Binary.from_uuid(element.id),
            "subreddit": element.subreddit,
            "watch": element.watch,
        }

    def _deserialize(self, raw_data: Dict[str, any]) -> Watchable:
        return Watchable(
            id=raw_data["_id"].as_uuid(),
            subreddit=raw_data["subreddit"],
            watch=raw_data["watch"],
        )
