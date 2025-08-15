from typing import List
from uuid import UUID, uuid4

from app.domain.aggregates.template import TemplateAggregate
from app.domain.exceptions.template import TemplateNotFoundError
from app.domain.repositories.template import TemplateRepository


class TemplateRepositoryMock(TemplateRepository):
    data: List[TemplateAggregate] = []

    async def create(self, entity: TemplateAggregate) -> TemplateAggregate:
        new_template = TemplateAggregate(
            id=uuid4(),
            title=entity.title,
            description=entity.description,
        )
        self.data.append(new_template)
        return new_template

    async def get_by_id(self, entity_id: UUID) -> TemplateAggregate | None:
        template = next(
            (template for template in self.data if template.id == entity_id), None
        )
        if not template:
            raise TemplateNotFoundError(f"Template {entity_id} not found")
        return template

    async def get_all(self) -> List[TemplateAggregate]:
        return self.data

    async def update(self, entity: TemplateAggregate) -> TemplateAggregate:
        pass

    async def delete(self, entity_id: UUID) -> bool:
        pass
