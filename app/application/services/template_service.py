from uuid import UUID

from app.application.dtos.section import CreateSectionDTO
from app.domain.aggregates.template import TemplateAggregate
from app.domain.entities.section import SectionEntity
from app.domain.repositories.unit_of_work import AbstractUnitOfWork


class TemplateNotFoundError(Exception):
    pass


async def create_template(
    uow: AbstractUnitOfWork,
    title: str,
    description: str | None = None,
) -> TemplateAggregate:
    new_template = await uow.template.create(
        TemplateAggregate(title=title, description=description)
    )
    await uow.commit()
    return new_template


async def publish_template(
    uow: AbstractUnitOfWork,
    template_id: UUID,
) -> TemplateAggregate:
    template = await uow.template.get_by_id(template_id)
    template.publish()
    await uow.template.update(template)
    await uow.commit()
    return template


async def add_section(
    uow: AbstractUnitOfWork,
    template_id: UUID,
    data: CreateSectionDTO,
) -> TemplateAggregate:
    template = await uow.template.get_by_id(template_id)
    template.add_section(SectionEntity(title=data.title, description=data.description))
    await uow.template.update(template)
    await uow.commit()
    return template
