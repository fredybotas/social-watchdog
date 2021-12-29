from abc import ABC, abstractmethod
import bson
from typing import Generic, TypeVar, Optional, Dict, List
from pymongo import MongoClient
import copy
from uuid import UUID

T = TypeVar("T")
DATABASE_NAME = "reddit_watchdog"


class IGenericRepository(ABC, Generic[T]):
    @abstractmethod
    def get_one(self, filter: Dict[str, any]) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self, filter: Dict[str, any]) -> List[T]:
        pass

    @abstractmethod
    def insert_one(self, value: T) -> None:
        pass

    @abstractmethod
    def remove(self, id: str) -> None:
        pass

    @abstractmethod
    def update_one(self, value: T) -> Optional[T]:
        pass


class GenericMongoRepository(IGenericRepository):
    def __init__(self, client: MongoClient, table_name: str) -> None:
        super().__init__()
        self.table_name = table_name
        self.handle = client.get_database(DATABASE_NAME).get_collection(table_name)

    @staticmethod
    def _prepare_filter(filter: Dict[str, any]) -> Dict[str, any]:
        altered_filter = copy.deepcopy(filter)
        if "id" in filter:
            altered_filter["_id"] = bson.Binary.from_uuid(UUID(filter["id"]))
            altered_filter.pop("id")
        return altered_filter

    def _serialize(self, element: T) -> Dict[str, any]:
        raise NotImplementedError()

    def _deserialize(self, raw_data: Dict[str, any]) -> T:
        raise NotImplementedError()

    def get_one(self, filter: Dict[str, any]) -> Optional[T]:
        result = self.handle.find_one(GenericMongoRepository._prepare_filter(filter))
        if result is None:
            return result
        return self._deserialize(result)

    def get_all(self, filter: Dict[str, any]) -> List[T]:
        return [
            self._deserialize(element)
            for element in self.handle.find(
                GenericMongoRepository._prepare_filter(filter)
            )
        ]

    def insert_one(self, value: T) -> None:
        self.handle.insert_one(self._serialize(value))

    def remove(self, id: str) -> None:
        self.handle.delete_one({"_id": bson.Binary.from_uuid(UUID(id))})

    def update_one(self, value: T) -> Optional[T]:
        self.handle.replace_one(
            {"_id": bson.Binary.from_uuid(value.id)}, self._serialize(value)
        )
