from abc import ABC, abstractmethod
import bson
from typing import Generic, TypeVar, Optional, Dict
from pymongo import MongoClient

T = TypeVar("T")
DATABASE_NAME = "reddit_watchdog"


class IGenericRepository(ABC, Generic[T]):
    @abstractmethod
    def get_one(self, id: str) -> Optional[T]:
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

    def _serialize(self, element: T) -> Dict:
        pass

    def _deserialize(self, raw_data: Dict[str, any]) -> T:
        pass

    def get_one(self, id: str) -> Optional[T]:
        result = self.handle.find_one(bson.Binary.from_uuid(id))
        if result is None:
            return result
        return self._deserialize(result)

    def insert_one(self, value: T) -> None:
        self.handle.insert_one(self._serialize(value))

    def remove(self, id: str) -> None:
        self.handle.delete_one({"_id": bson.Binary.from_uuid(id)})

    def update_one(self, value: T) -> Optional[T]:
        self.handle.replace_one(
            {"_id": bson.Binary.from_uuid(value.id)}, self._serialize(value)
        )
