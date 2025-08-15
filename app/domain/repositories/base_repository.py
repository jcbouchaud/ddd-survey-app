from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar
from uuid import UUID

from ..entities.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(Generic[T], ABC):
    @abstractmethod
    async def create(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:
        raise NotImplementedError
