from app.domain.repositories.unit_of_work import AbstractUnitOfWork
from app.infrastructure.persistence.unit_of_work_mock import UnitOfWorkMock


def get_uow() -> AbstractUnitOfWork:
    return UnitOfWorkMock()
