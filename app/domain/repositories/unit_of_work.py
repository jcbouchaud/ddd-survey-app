from abc import ABC, abstractmethod

from .template import TemplateRepository


class AbstractUnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self) -> "AbstractUnitOfWork":
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

    @property
    def template(self) -> TemplateRepository:
        raise NotImplementedError
