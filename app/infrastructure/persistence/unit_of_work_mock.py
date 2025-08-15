from app.domain.repositories.template import TemplateRepository
from app.domain.repositories.unit_of_work import AbstractUnitOfWork

from .template_repository_mock import TemplateRepositoryMock


class UnitOfWorkMock(AbstractUnitOfWork):
    def __init__(self):
        self._template: TemplateRepository | None = None
        self._committed = False

    async def __aenter__(self) -> "UnitOfWorkMock":
        self._template = TemplateRepositoryMock()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        self._committed = True

    async def rollback(self) -> None:
        self._committed = False
        self._template = TemplateRepositoryMock()

    @property
    def template(self) -> TemplateRepository:
        if self._template is None:
            raise RuntimeError("Unit of Work not initialized with template repository")
        return self._template
